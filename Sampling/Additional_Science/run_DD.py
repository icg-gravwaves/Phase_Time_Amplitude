import subprocess

def main():
    cmd = [
        "python", "Detector_dependent.py",
        "--ifos", "L1", "H1", "V1",  
        "--all-ifos", "L1", "H1", "V1",
        "--relative-sensitivities", "1.0", "0.94", "0.32", 
        "--samples", "300000.",
        "--batch-size", "1000000",
        "--seed", "105",
        "--output-file", "../../Files/Det_Dep/HLV_Samples_DD.hdf",
        "--verbose"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()