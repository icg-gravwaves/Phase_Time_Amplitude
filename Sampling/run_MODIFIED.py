import subprocess

def main():
    cmd = [
        "python", "PTA_sampling_MODIFIED.py",
        "--ifos", "H1", "L1", 
        "--relative-sensitivities", "1.0", "1.0",
        "--snr-ratio", "4.",
        "--snr-reference", "6.",
        "--snr-uncertainty", "1.",
        "--timing-uncertainty", "0.0005",
        "--sample-size", "100000000",
        "--batch-size", "10000000",
        "--seed", "11",
        "--output-file", "../Files/HL_MOD_Samples.hdf",
        "--bin-density", "4",
        "--weight-threshold", "0.0001",
        "--smoothing-sigma", "5",
        "--param-bin-dtype", "int32",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()