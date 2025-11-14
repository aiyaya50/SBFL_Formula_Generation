import pandas as pd
import numpy as np
import os

# === CONFIG ===
granularities = ["Line", "Method", "Class"]
projects = {"Lang": 65, "Chart": 26, "Mockito": 38, "Time": 27, "Math": 106}  # project: number_of_bugs
projects = {"Lang": 65, "Chart": 26, "Mockito": 38, "Time": 27, "Math": 106, 'Collections':28, 'Codec':18, 'Csv': 16, 'Cli': 40,'JxPath': 22, \
          'Jsoup': 93, 'JacksonXml': 6,'JacksonDatabind': 112, 'JacksonCore': 26, 'Gson': 18, 'Compress': 47}
metrics = ["barinel","dstar","jaccard","meco","ochiai","ochiai2","opt",
           "tarantula","sgf_1","sgf_2","fo1","fo2","fo7","fo8","fo17"]
#metrics = ["AnomalyScore"]


# === FUNCTION TO EVALUATE METRIC PER BUG ===
def evaluate_formula(df, metric):
    """
    Compute Top-1, Top-3, Top-5, EXAM, MFR, MAR for a single metric on one bug.
    MAR = Mean Average Rank of all buggy lines.
    MFR = first buggy line rank.
    """

    if metric not in df.columns:
        return {"Top-1": np.nan, "Top-3": np.nan, "Top-5": np.nan,
                "EXAM": np.nan, "MFR": np.nan, "MAR": np.nan}

    df = df.copy()
    df = df.dropna(subset=[metric])
    # Convert metric to numeric; replace Inf/-Inf with NaN
    df[metric] = pd.to_numeric(df[metric], errors="coerce")

    finite_vals = df[metric].replace([np.inf, -np.inf], np.nan)
    max_finite = finite_vals.max()+1
    min_finite = finite_vals.min()-1
    df[metric] = df[metric].replace(np.inf, max_finite)
    df[metric] = df[metric].replace(-np.inf, min_finite)


    if df.empty:
        return {"Top-1": 0, "Top-3": 0, "Top-5": 0,
                "EXAM": np.nan, "MFR": np.nan, "MAR": np.nan}

    # Rank statements by suspiciousness, placing NaN at bottom
    df["rank"] = df[metric].rank(ascending=False, method="dense", na_option='bottom')
    df = df.dropna(subset=[metric])
    buggy_ranks = df[df["label"] == 1]["rank"].tolist()
    if not buggy_ranks:
        return {"Top-1": 0, "Top-3": 0, "Top-5": 0,
                "EXAM": np.nan, "MFR": np.nan, "MAR": np.nan}

    best_rank = min(buggy_ranks)
    top1 = int(best_rank <= 1)
    top3 = int(best_rank <= 3)
    top5 = int(best_rank <= 5)
    exam = best_rank / len(df)
    MFR = best_rank
    MAR = np.mean(buggy_ranks)
    ranked_indices = df.sort_values(metric, ascending=False).index.tolist()
    first_bug_pos = next(i for i, idx in enumerate(ranked_indices, start=1) if df.loc[idx, "label"] == 1)
    exam = (first_bug_pos - 1) / len(df)
    return {"Top-1": top1, "Top-3": top3, "Top-5": top5,
            "EXAM": exam, "MFR": MFR, "MAR": MAR}



# === MAIN PIPELINE ===
for granularity in granularities:
    print (f'~~~~~~~~{granularity}~~~~~~~~~~~')
    base_path = f"/media/sf_shared_coding/ML Tutorial/myFLs/{granularity}/SBFL"
    base_path = f"/home/aiyaya50/myFL/myFLData/{granularity}/SBFL"
    #/home/aiyaya50/myFL/myFLData/Line/SBFL
    os.makedirs(f"{granularity}_level", exist_ok=True)

    all_bug_results = []
    project_results = {}

    for project, num_bugs in projects.items():
        print(f"\n%%%% Project {project} %%%%")
        project_scores = {m: {"Top-1": [], "Top-3": [], "Top-5": [], "EXAM": [], "MFR": [], "MAR": []} for m in metrics}

        for bug_id in range(1, num_bugs + 1):
            bug_file = os.path.join(base_path, f"{project}-{bug_id}.csv")
            if not os.path.exists(bug_file):
                print(f"Missing file: {bug_file}")
                continue

            try:
                df = pd.read_csv(bug_file)
            except Exception as e:
                print(f"Error reading {bug_file}: {e}")
                continue

            bug_row = {"Project": project, "Bug": bug_id}

            for m in metrics:
                scores = evaluate_formula(df, m)
                for key, val in scores.items():
                    project_scores[m][key].append(val)
                    bug_row[f"{m}_{key}"] = val

            all_bug_results.append(bug_row)

        # Aggregate per project
        agg = {}
        for m in metrics:
            agg[m] = {}
            for k, v in project_scores[m].items():
                if k in ["MFR", "MAR", "EXAM"]:
                    agg[m][k] = np.nanmean(v)
                else:
                    agg[m][k] = np.nansum(v)
        project_results[project] = agg

    # === SAVE PER-BUG RESULTS ===
    df_bugs = pd.DataFrame(all_bug_results)
    df_bugs.to_csv(f"{granularity}_level/all_bugs_results.csv", index=False)
    print("Saved all_bugs_results.csv")

    # === SAVE PER-PROJECT RESULTS ===
    project_dfs = []
    for project, agg in project_results.items():
        df_proj = pd.DataFrame(agg).T  # metrics as rows
        df_proj.to_csv(f"{granularity}_level/{project}_results.csv")
        df_proj["Project"] = project
        project_dfs.append(df_proj)
        print(f"Saved {project}_results.csv")

    # === AGGREGATE ACROSS ALL PROJECTS (equal weight per project) ===
    # === AGGREGATE ACROSS ALL PROJECTS ===
    df_all_projects = pd.concat(project_dfs)

    agg_global = {}
    for m in metrics:
        agg_global[m] = {}
        for k in ["Top-1", "Top-3", "Top-5", "EXAM", "MFR", "MAR"]:
            values = df_all_projects.loc[m, k] if isinstance(df_all_projects.loc[m, k], pd.Series) else [df_all_projects.loc[m, k]]

            if k in ["MFR", "MAR", "EXAM"]:
                agg_global[m][k] = np.nanmean(values)
            else:  # Top-N
                agg_global[m][k] = np.nansum(values)

    df_global = pd.DataFrame(agg_global).T
    df_global.to_csv(f"{granularity}_level/ALL_PROJECTS_results.csv")
    print("Saved ALL_PROJECTS_results.csv")
