namespace IKT300;

public class Kernel
{
    bool running = true;
    double oldTime;
    double programTime = 0;
    double fps = 60;

    List<Plugin> plugins = new();
    public void AddPlugin(Plugin plugin)
    {
        plugins.Add(plugin);
    }
    public void Run()
    {
        Console.WriteLine("Greetings, Universe");
        oldTime = CurrentTime();
        int timeToRun = 300;
        while (running)
        {
            double deltaTime = CurrentTime() - oldTime;
            oldTime = CurrentTime();

            programTime += deltaTime;
            if (programTime >= 1 / fps)
            {
                programTime -= 1 / fps;
                for (int i = plugins.Count - 1; i >= 0; i--)
                {
                    if (plugins[i].HeartMonitor() == 1)
                    {
                        plugins[i].Process();
                    }
                    else
                    {
                        Console.WriteLine("plugin did not work");
                        plugins.RemoveAt(i);
                    }
                }
                if (timeToRun-- < 0)
                {
                    running = false;
                }
            }
        }
    }
    private double CurrentTime()
    {
        return DateTime.Now.TimeOfDay.TotalSeconds;
    }

}