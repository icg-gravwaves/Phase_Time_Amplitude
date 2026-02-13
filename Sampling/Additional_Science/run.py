import subprocess

def main():
    cmd = [
        "python", "EW_samples.py",
        "--ifos", "L1", "H1",
        "--relative-sensitivities", "1.0", "0.94", 
        "--samples", "200000.",
        "--batch-size", "1000000",
        "--seed", "105",
        "--output-file", "../../Files/EW/HL_Samples_EW.hdf",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()