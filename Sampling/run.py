import subprocess

def main():
    cmd = [
        "python", "PTASNR_samples.py",
        "--ifos", "H1", "V1", 
        "--relative-sensitivities", "0.94", "0.32", 
        "--samples", "500000.",
        "--batch-size", "1000000",
        "--seed", "105",
        "--output-file", "../Files/PTASNR/HV_Samples_Flow.hdf",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()