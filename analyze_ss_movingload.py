import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

def analyze_beam(L, W1, W2, x):
    max_reaction_A = 0
    max_reaction_B = 0
    BM_01 = 0
    SF_01 = 0
    BM_max = 0
    SF_max = 0
    z_location_BM_max = 0
    y_location_SF_max = 0

    step = 0.1
    positions = [round(p, 2) for p in list(frange(0, L - x, step))]

    for a in positions:
        b = a + x
        RA = (W1 * (L - a) + W2 * (L - b)) / L
        RB = W1 + W2 - RA
        max_reaction_A = max(max_reaction_A, RA)
        max_reaction_B = max(max_reaction_B, RB)

        if a == 0:
            BM_01 = RA * a

        if round(a, 2) <= L / 2 < round(b, 2):
            SF_01 = RA - W1

        for z in [round(i, 2) for i in list(frange(0, L, step))]:
            if a <= z <= b:
                BM = RA * z - W1 * (z - a)
                SF = RA
            elif z < a:
                BM = RA * z
                SF = RA
            else:
                BM = RA * z - W1 * (z - a) - W2 * (z - b)
                SF = RA - W1 - W2

            if BM > BM_max:
                BM_max = BM
                z_location_BM_max = z
            if abs(SF) > abs(SF_max):
                SF_max = SF
                y_location_SF_max = z

    return {
        "Max Reaction A": round(max_reaction_A, 2),
        "Max Reaction B": round(max_reaction_B, 2),
        "BM_01": round(BM_01, 2),
        "SF_01": round(SF_01, 2),
        "BM_max": round(BM_max, 2),
        "BM_max at z (m)": round(z_location_BM_max, 2),
        "SF_max": round(SF_max, 2),
        "SF_max at y (m)": round(y_location_SF_max, 2)
    }

def compute_sfd_bmd(L, W1, W2, x):
    dx = 0.1
    x_vals = [i * dx for i in range(int(L / dx) + 1)]
    sfd = []
    bmd = []

    a = (L - x) / 2
    b = a + x

    RA = (W1 * (L - a) + W2 * (L - b)) / L

    for xi in x_vals:
        sf = RA
        if xi >= a:
            sf -= W1
        if xi >= b:
            sf -= W2
        sfd.append(sf)

        bm = RA * xi
        if xi >= a:
            bm -= W1 * (xi - a)
        if xi >= b:
            bm -= W2 * (xi - b)
        bmd.append(bm)

    return x_vals, sfd, bmd

class BeamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Beam Analysis - Two Point Moving Loads")

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.inputs = {}
        for label in ["Beam Length (L)", "Load W1 (kN)", "Load W2 (kN)", "Distance between Loads (x)"]:
            left_layout.addWidget(QLabel(label))
            line_edit = QLineEdit()
            self.inputs[label] = line_edit
            left_layout.addWidget(line_edit)

        self.calc_btn = QPushButton("Analyze Beam")
        self.calc_btn.clicked.connect(self.calculate)
        left_layout.addWidget(self.calc_btn)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        left_layout.addWidget(self.result)

        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        right_layout.addWidget(self.canvas)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        self.setLayout(main_layout)

    def calculate(self):
        try:
            L = float(self.inputs["Beam Length (L)"].text())
            W1 = float(self.inputs["Load W1 (kN)"].text())
            W2 = float(self.inputs["Load W2 (kN)"].text())
            x = float(self.inputs["Distance between Loads (x)"].text())

            result = analyze_beam(L, W1, W2, x)
            self.result.clear()
            for k, v in result.items():
                self.result.append(f"{k}: {v}")

            x_vals, sfd, bmd = compute_sfd_bmd(L, W1, W2, x)

            self.canvas.figure.clear()

            # SFD plot
            ax1 = self.canvas.figure.add_subplot(211)
            ax1.step(x_vals, sfd, where='post', color='blue', label='SFD')
            ax1.axhline(0, color='gray', linestyle='--', linewidth=1)

            max_sf = max(sfd, key=abs)
            max_sf_index = sfd.index(max_sf)
            ax1.plot(x_vals[max_sf_index], max_sf, 'bo')
            ax1.annotate(f'Max SF = {round(max_sf, 2)} kN',
                         xy=(x_vals[max_sf_index], max_sf),
                         xytext=(x_vals[max_sf_index] + 0.5, max_sf),
                         arrowprops=dict(facecolor='blue', arrowstyle='->'),
                         fontsize=9)

            ax1.set_title("Shear Force Diagram")
            ax1.set_xlabel("Beam Length (m)")
            ax1.set_ylabel("Shear Force (kN)")
            ax1.grid(True)

            # BMD plot
            ax2 = self.canvas.figure.add_subplot(212)
            ax2.plot(x_vals, bmd, color='red', label='BMD')
            ax2.axhline(0, color='gray', linestyle='--', linewidth=1)

            max_bm = max(bmd)
            max_bm_index = bmd.index(max_bm)
            ax2.plot(x_vals[max_bm_index], max_bm, 'ro')
            ax2.annotate(f'Max BM = {round(max_bm, 2)} kNm',
                         xy=(x_vals[max_bm_index], max_bm),
                         xytext=(x_vals[max_bm_index] + 0.5, max_bm),
                         arrowprops=dict(facecolor='red', arrowstyle='->'),
                         fontsize=9)

            ax2.set_title("Bending Moment Diagram")
            ax2.set_xlabel("Beam Length (m)")
            ax2.set_ylabel("Bending Moment (kNm)")
            ax2.grid(True)

            self.canvas.draw()

        except Exception as e:
            self.result.setText(f"Error: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BeamApp()
    window.show()
    sys.exit(app.exec_())
