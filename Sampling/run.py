import subprocess

def main():
    cmd = [
        "python", "PTA_samples.py",
        "--ifos", "H1",  "L1",
        "--relative-sensitivities", "1.0", "1.0",
        "--samples", "300000.",
        "--batch-size", "1000000",
        "--seed", "105",
        "--output-file", "../Files/HL_Samples.hdf",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()