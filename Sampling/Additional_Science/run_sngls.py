import subprocess

def main():
    cmd = [
        "python", "Sngls_Samples.py",
        "--ifos", "H1",
        "--relative-sensitivities", "0.94",
        "--samples", "300000.",
        "--batch-size", "1000000",
        "--seed", "105",
        "--output-file", "../Files/PTASNR/H_Samples_Flow.hdf",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()