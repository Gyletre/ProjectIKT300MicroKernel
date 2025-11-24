
using System;
using System.Diagnostics;
using IKT300.Plugins;
using IKT300;


public class MicroKernel
{
    private static void Main()
    {
        Kernel kernel = new Kernel();
        new TestPlugin(kernel);
        new GUIPlugin(kernel);
        kernel.Run();
    }
}
