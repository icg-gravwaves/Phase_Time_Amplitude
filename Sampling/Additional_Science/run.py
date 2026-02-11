import subprocess

def main():
    cmd = [
        "python", "PTA_samples.py",
        "--ifos", "H1", "L1", "K1",
        "--relative-sensitivities", "1.0", "1.0", "1.0", 
        "--samples", "500000.",
        "--batch-size", "1000000",
        "--seed", "105",
        "--output-file", "../Files/4det/HLK_Samples_Flow.hdf",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()