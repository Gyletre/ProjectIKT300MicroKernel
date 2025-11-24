using System;
namespace IKT300
{
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
        public abstract void Process();
    }
}

namespace IKT300.Plugins
{
    public class TestPlugin : Plugin
    {
        public TestPlugin(Kernel k) : base(k)
        {
        }

        public override void Process()
        {
            Console.WriteLine("Testing");
        }
    }
}
