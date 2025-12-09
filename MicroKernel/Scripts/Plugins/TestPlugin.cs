using System;

namespace IKT300.Plugins
{
    public class TestPlugin : Plugin
    {
        public TestPlugin(Kernel k) : base(k)
        {
        }
        public  override void Start(){
            Console.WriteLine("Test plugin has started");
        }

        public override void Stop(){
            Console.WriteLine("Test plugin has stopped");
        }
        
        
        public override void Process()
        {
            Console.WriteLine("Testing");
        }
    }
}
