using System.Diagnostics;

namespace IKT300.Plugins
{
    public class ExternalPlugin : Plugin
    {
        string filePath;
        Process process;

        public ExternalPlugin(Kernel k, string path) : base(k)
        {
            filePath = path;
        }

        public override void Start()
        {
            try
            {
                process = Process.Start(filePath);
                Console.WriteLine("Startet ekstern: " + filePath);
            }
            catch
            {
                Console.WriteLine("Klarte ikke starte: " + filePath);
            }
        }

        public override void Stop()
        {
            if (process != null && !process.HasExited)
            {
                process.Kill();
                Console.WriteLine("Stoppet ekstern: " + filePath);
            }
        }

        public override int HeartMonitor()
        {
            if (process == null || process.HasExited)
            {
                return 0; // Død
            }
            return 1; // Lever
        }

        public override void Process()
        {
            // Eksterne programmer kjører av seg selv
        }
    }
}
