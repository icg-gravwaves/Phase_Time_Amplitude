import subprocess

def main():
    cmd = [
        "python", "PTA_samples.py",
        "--ifos", "H1",  "L1", "V1", 
        "--relative-sensitivities", "1.0", "1.0", "0.33", 
        "--samples", "500000.",
        "--batch-size", "1000000",
        "--seed", "105",
        "--output-file", "../Files/HLV_Samples_Flow.hdf",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()