import subprocess

def main():
    cmd = [
        "python", "PTA_sampling_MODIFIED.py",
        "--ifos", "H1", "V1",
        "--relative-sensitivities", "0.94", "0.32",
        "--snr-ratio", "4.",
        "--snr-reference", "4.",
        "--snr-uncertainty", "1.",
        "--timing-uncertainty", "0.0005",
        "--sample-size", "100000000",
        "--batch-size", "1000000",
        "--seed", "2",
        "--output-file", "../Files/hvtest.hdf",
        "--bin-density", "4",
        "--weight-threshold", "0.0001",
        "--smoothing-sigma", "5",
        "--param-bin-dtype", "int32",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()