import subprocess

def main():
    cmd = [
        "python", "PTA_samples.py",
        "--ifos", "L1","H1", "V1", "K1" , "A1",
        "--relative-sensitivities", "1.0","1.0", "1.0", "1.0", "1.0",
        "--samples", "1000000.",
        "--batch-size", "1000000",
        "--seed", "105",
        "--output-file", "../Files/HLVKI_Samples_Flow.hdf",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()