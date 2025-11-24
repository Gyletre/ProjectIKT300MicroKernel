using System;

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
