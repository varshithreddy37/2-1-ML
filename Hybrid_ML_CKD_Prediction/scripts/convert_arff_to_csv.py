import pandas as pd
import re

input_file = "chronic_kidney_disease.arff"
output_file = "chronic_kidney_disease.csv"

attributes = []
data_rows = []
data_started = False

# Read ARFF file
with open(input_file, "r", encoding="utf-8", errors="replace") as file:

    for line_number, line in enumerate(file, start=1):

        line = line.strip()

        # Ignore empty lines and comments
        if not line or line.startswith("%"):
            continue

        # Read attribute names
        if line.lower().startswith("@attribute"):

            match = re.match(
                r"@attribute\s+['\"]?([^'\"]+)['\"]?\s+",
                line,
                re.IGNORECASE
            )

            if match:
                attributes.append(match.group(1).strip())

        # Start of data
        elif line.lower() == "@data":
            data_started = True

        # Read data
        elif data_started:

            values = [value.strip() for value in line.split(",")]

            # Remove extra empty value caused by trailing comma
            if len(values) == len(attributes) + 1 and values[-1] == "":
                values = values[:-1]

            # Check number of columns
            if len(values) != len(attributes):

                print(
                    f"Skipping problematic row at line {line_number}: "
                    f"{len(values)} values found, "
                    f"{len(attributes)} expected"
                )

                continue

            data_rows.append(values)


# Create DataFrame
df = pd.DataFrame(data_rows, columns=attributes)

# Replace ? with missing values
df = df.replace("?", pd.NA)

# Save CSV
df.to_csv(output_file, index=False)

print()
print("======================================")
print("CSV FILE CREATED SUCCESSFULLY!")
print("======================================")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print()
print("Column names:")
print(df.columns.tolist())
print()
print("Output file:")
print(output_file)