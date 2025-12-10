import pandas as pd

def load_jobs(csv_path="data/jobs_sample.csv"):
    """
    Loads job postings from a CSV file and returns a list of dictionaries.
    """
    try:
        df = pd.read_csv(csv_path)
        df["description"] = df["description"].fillna("")
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading jobs: {e}")
        return []

# Test
if __name__ == "__main__":
    jobs = load_jobs()
    print("Loaded jobs:", len(jobs))
    print(jobs[0])
