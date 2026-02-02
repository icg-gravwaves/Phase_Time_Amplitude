import subprocess

def main():
    cmd = [
        "python", "PTASNR_samples.py",
        "--ifos", "L1", "H1","V1",
        "--relative-sensitivities", "1.0", "0.94","0.32",
        "--samples", "500000.",
        "--batch-size", "1000000",
        "--seed", "105",
        "--output-file", "../Files/PTASNR/LHV_Samples_Flow.hdf",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()