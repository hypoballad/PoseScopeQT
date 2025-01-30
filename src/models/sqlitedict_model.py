import sqlitedict
import pickle
import numpy as np

class SqliteDictModel:
    def __init__(self, db_path: str):
        self.db = sqlitedict.SqliteDict(db_path, autocommit=True)
        self._initialize_defaults()

    def _initialize_defaults(self):
        defaults = {
            "camera0": "0",
            "camera1": "1",
            "frame_width": "1920",
            "frame_height": "1080",
            "mono_calibration_frames": "10",
            "stereo_calibration_frames": "10",
            "view_resize": "2",
            "checkerboard_box_size_scale": "3.4",
            "checkerboard_rows": "4",
            "checkerboard_columns": "7",
            "cooldown": "100"
        }
        for key, value in defaults.items():
            if key not in self.db:
                self.db[key] = value

    def __getitem__(self, key):
        return self.db.get(key, "")

    def __setitem__(self, key, value):
        self.db[key] = value
    
    def save_numpy_array_to_sqlitedict(self, key, array):
        # NumPy 配列をシリアライズ
        serialized_array = pickle.dumps(array)
        # シリアライズされた配列を保存
        self.db[key] = serialized_array

    def load_numpy_array_from_sqlitedict(self, key):
        # シリアライズされた配列を取得
        serialized_array = self.db[key]
        # NumPy 配列をデシリアライズ
        array = pickle.loads(serialized_array)
        return array

    def close(self):
        self.db.close()

    def save_camera_intrinsics(self, camera_matrix, distortion_coefs, camera_name):
        """
        SQLite にカメラの内部パラメータと歪み係数を保存する。
        
        Args:
            db_path (str): SQLite データベースのパス。
            camera_matrix (np.ndarray): カメラの内部行列。
            distortion_coefs (np.ndarray): 歪み係数。
            camera_name (str): カメラ名。
        """
        self.save_numpy_array_to_sqlitedict(f"{camera_name}_intrinsic", camera_matrix)
        self.save_numpy_array_to_sqlitedict(f"{camera_name}_distortion", distortion_coefs)


    def read_camera_params(self, camera_name):
        """
        SQLite からカメラの内部パラメータと歪み係数を読み込む。
        
        Args:
            db_path (str): SQLite データベースのパス。
            camera_name (str): カメラ名。
        
        Returns:
            tuple[np.ndarray, np.ndarray]: カメラ行列 (cmtx), 歪み係数 (dist)
        """
        cmtx = self.load_numpy_array_from_sqlitedict(f"{camera_name}_intrinsic")
        dist = self.load_numpy_array_from_sqlitedict(f"{camera_name}_distortion")
        return cmtx, dist

    def save_extrinsic_calibration_parameters(self, R, T, camera_name):
        self.save_numpy_array_to_sqlitedict(f"{camera_name}_R", R)
        self.save_numpy_array_to_sqlitedict(f"{camera_name}_T", T)

    def read_extrinsic_calibration_parameters(self, camera_name):
        R = self.load_numpy_array_from_sqlitedict(f"{camera_name}_R")
        T = self.load_numpy_array_from_sqlitedict(f"{camera_name}_T")
        return R, T


def migrate_from_file_to_sqlitedict(file_path, db_path, camera_name):
    """
    既存のカメラパラメータファイルを SQLite に移行する。
    
    Args:
        file_path (str): 既存のカメラパラメータファイルのパス。
        db_path (str): SQLite データベースのパス。
        camera_name (str): カメラ名。
    """
    intrinsic_data = []
    distortion_data = []
    mode = None
    
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if "intrinsic:" in line:
                mode = "intrinsic"
                continue
            elif "distortion:" in line:
                mode = "distortion"
                continue

            if mode == "intrinsic":
                intrinsic_data.append(list(map(float, line.split())))
            elif mode == "distortion":
                distortion_data.extend(map(float, line.split()))
    import numpy as np
    cmtx = np.array(intrinsic_data, dtype=np.float64)
    dist = np.array([distortion_data], dtype=np.float64)
    db = SqliteDictModel(db_path)
    db.save_camera_intrinsics(cmtx, dist, camera_name)
    print(f"Successfully migrated data from {file_path} to {db_path}")

def migrate_extrinsic_from_file_to_sqlitedict(file_path, db_path, camera_name):
    """
    既存の外部カメラパラメータファイルを SQLite に移行する。
    """
    R_data = []
    T_data = []
    mode = None
    
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if "R:" in line:
                mode = "R"
                continue
            elif "T:" in line:
                mode = "T"
                continue

            if mode:
                values = list(map(float, line.split()))
                if mode == "R" and len(values) == 3:
                    R_data.append(values)
                elif mode == "T" and len(values) == 1:
                    T_data.append(values[0])

    if len(R_data) == 3:  # Rotation matrix
        R = np.array(R_data, dtype=np.float64)
    else:
        raise ValueError("Invalid rotation matrix data format in file")

    if len(T_data) == 3:  # Translation vector
        T = np.array(T_data, dtype=np.float64).reshape((3, 1))
    else:
        raise ValueError("Invalid translation vector data format in file")

    db = SqliteDictModel(db_path)
    db.save_extrinsic_calibration_parameters(R, T, camera_name)
    print(f"Successfully migrated extrinsic data from {file_path} to {db_path}")

if __name__ == "__main__":
    import os
    db_path = "../PoseScopeQT.sqlite"
    if not os.path.exists(db_path):
        print("sqlite3 database file not found.")
        exit()
    # file_path0 = "../calibration_parameters/camera0_intrinsics.dat"
    # if not os.path.exists(file_path0):
    #     print("camera0_intrinsics.dat file not found.")
    #     exit()
    camera0_name = "camera0"
    # file_path1 = "../calibration_parameters/camera1_intrinsics.dat"
    # if not os.path.exists(file_path1):
    #     print("camera1_intrinsics.dat file not found.")
    camera1_name = "camera1"
    
    # migrate_from_file_to_sqlitedict(file_path0, db_path, camera0_name)
    # migrate_from_file_to_sqlitedict(file_path1, db_path, camera1_name)
    db = SqliteDictModel(db_path)
    # # 読み込み確認
    # cmtx0, dist0 = db.read_camera_params(camera0_name)
    # print("Loaded Camera Matrix:")
    # print(cmtx0)
    # print("\nLoaded Distortion Coefficients:")
    # print(dist0)
    # cmtx1, dist1 = db.read_camera_params(camera1_name)
    # print("Loaded Camera Matrix:")
    # print(cmtx1)
    # print("\nLoaded Distortion Coefficients:")
    # print(dist1)


    param_file_path0 = "../camera_parameters/camera0_rot_trans.dat"
    if not os.path.exists(param_file_path0):
        print("camera0_rot file not found.")
        exit()

    param_file_path1 = "../camera_parameters/camera1_rot_trans.dat"
    if not os.path.exists(param_file_path1):
        print("camera1_rot file not found.")
        exit()
    
    migrate_extrinsic_from_file_to_sqlitedict(param_file_path0, db_path, camera0_name)
    migrate_extrinsic_from_file_to_sqlitedict(param_file_path1, db_path, camera1_name)
    R0, T0 = db.read_extrinsic_calibration_parameters(camera0_name)
    print("caemra0")
    print("Loaded R0:")
    print(R0)
    print("\nLoaded T0:")
    print(T0)
    
    R1, T1 = db.read_extrinsic_calibration_parameters(camera1_name)
    print("camera1")
    print("\nLoaded R1:")
    print(R1)
    print("\nLoaded T1:")
    print(T1)
    db.close()
