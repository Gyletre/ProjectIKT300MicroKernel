using System.Diagnostics;
using System.Text.Json;
using IKT300.Plugins;

namespace IKT300.Launcher;
public class ExeLauncher : ILauncher
{
    string folderPath;
    public ExeLauncher(string path){
        folderPath =path;
    }

    public void RunPlugins(Kernel kernel)
    {
        string[] files = Directory.GetFiles(folderPath, "*.json");
        foreach (string file in files){
            string json = File.ReadAllText(file);
            PluginConfig config = JsonSerializer.Deserialize<PluginConfig>(json);
            if (config != null){
                new ExternalPlugin(kernel, config.FilePath);
            }
        }
    }
}
