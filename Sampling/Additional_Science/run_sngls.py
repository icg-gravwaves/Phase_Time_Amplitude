import subprocess

def main():
    cmd = [
        "python", "Sngls_Samples.py",
        "--ifos", "V1",
        "--relative-sensitivities", "0.32",
        "--samples", "300000.",
        "--batch-size", "1000000",
        "--seed", "105",
        "--output-file", "../../Files/PTASNR/V_Samples_Flow.hdf",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()