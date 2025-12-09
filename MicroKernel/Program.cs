
using System;
using System.Diagnostics;
using IKT300.Plugins;
using IKT300;


using IKT300.Launcher;

public class MicroKernel
{
    private static void Main()
    {
        Kernel kernel = new Kernel();

        // Lag launcher og gi den mappen med config filer
        string path = "PluginConfigs";
        ExeLauncher launcher = new ExeLauncher(path);
        kernel.SetLauncher(launcher);

        new TestPlugin(kernel);
        new GUIPlugin(kernel);
        kernel.Run();
    }
}
