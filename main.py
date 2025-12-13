from AnimeProccess.Config import RenameConfig, ConfigLoader
from AnimeProccess.Proccess import process_main


def main():
    conf: RenameConfig = ConfigLoader.load("conf.json")
    process_main(conf)

if __name__ == "__main__":
    main()