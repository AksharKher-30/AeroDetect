import os
import pandas as pd

def convert_csv_to_yolo(base_dir, class_map):
    """
    Convert CSV annotations (in YOLO format) to label text files for train, val, and test sets.

    Parameters:
    - base_dir (str): Path to the dataset folder that contains 'labels/train', 'labels/val', 'labels/test'.
    - class_map (dict): Dictionary mapping class names to class IDs.

    Example class_map:
        {
            "Drone": 0,
            "Helicopter": 1,
            "AirPlane": 2
        }
    """
    splits = ["train", "val", "test"]

    for split in splits:
        csv_path = os.path.join(base_dir, "labels", split, f"{split}_labels.csv")
        label_output_dir = os.path.join(base_dir, "labels", split)
        os.makedirs(label_output_dir, exist_ok=True)

        df = pd.read_csv(csv_path)

        grouped = df.groupby("filename")

        for filename, group in grouped:
            image_width = group.iloc[0]["width"]
            image_height = group.iloc[0]["height"]

            yolo_lines = []

            for _, row in group.iterrows():
                label = row["class"]

                if label not in class_map:
                    print(f"❌ Skipping unknown label '{label}' in file {filename}")
                    continue

                class_id = class_map[label]

                xmin, ymin, xmax, ymax = row["xmin"], row["ymin"], row["xmax"], row["ymax"]
                x_center = ((xmin + xmax) / 2) / image_width
                y_center = ((ymin + ymax) / 2) / image_height
                box_width = (xmax - xmin) / image_width
                box_height = (ymax - ymin) / image_height

                yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}"
                yolo_lines.append(yolo_line)

            txt_filename = os.path.splitext(filename)[0] + ".txt"
            label_file_path = os.path.join(label_output_dir, txt_filename)

            with open(label_file_path, "w") as f:
                f.write("\n".join(yolo_lines))

        print(f"✅ Converted {split}_labels.csv to YOLO format in {label_output_dir}")