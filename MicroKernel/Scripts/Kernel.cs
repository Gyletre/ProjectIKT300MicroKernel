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

    public void RestartPlugin(Plugin plugin){
        plugin.Stop();
        plugin.Start();}

    public void Run()
    {
        Console.WriteLine("Greetings, Universe");
        foreach  (Plugin plugin in  plugins){
            plugin.Start();
        }
        

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
                        RestartPlugin(plugins[i]);
                        if (plugins[i].HeartMonitor() == 1){
                            Console.WriteLine("Plugin has restarted successfully");
                        }
                        else{
                            plugins[i].Stop();
                            plugins.RemoveAt(i);}
                    }
                }
                if (timeToRun-- < 0)
                {
                    running = false;
                }
            }
        }

        foreach (Plugin plugin in plugins){
            plugin.Stop();
        }
    }
    private double CurrentTime()
    {
        return DateTime.Now.TimeOfDay.TotalSeconds;
    }

}
public abstract class Plugin
    {
        protected Kernel kernel;
        public Plugin(Kernel k)
        {
            kernel = k;
            kernel.AddPlugin(this);
        }
        public int HeartMonitor()
        {
            return 1;
        }
        public virtual void Start() {}
        public virtual void Stop() {}
        public abstract void Process();
    }