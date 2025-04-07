# Beam Analysis under Two-Point Moving Loads (PyQt5 Desktop App)

This Python application provides an interactive graphical user interface (GUI) to analyze simply supported beams subjected to two-point moving loads. Built with **PyQt5** and **Matplotlib**, it calculates support reactions, shear force, and bending moment values, and plots their respective diagrams.

## 🔧 Features

- 📐 Input beam length, load magnitudes, and distance between loads
- ⚙️ Computes:
  - Maximum reactions at supports
  - Shear force and bending moment at key locations
  - Maximum values and their positions
- 📊 Plots:
  - Shear Force Diagram (SFD)
  - Bending Moment Diagram (BMD)
- 🖱️ Simple, intuitive desktop GUI
- 📄 Real-time analysis output in text form

---

## 🖥️ GUI Preview

![image](https://github.com/user-attachments/assets/0cf08979-da5a-4b2f-9bf8-8a2d1f5e6e4e)


---

## 🧮 Theoretical Background

The application is based on classical structural analysis principles. Moving loads are shifted along the beam, and at each step, the reactions, shear forces, and bending moments are calculated. The maximum values from all positions are extracted to provide the worst-case design scenario.

---

## 📚 Literature & References


1. IS 800:2007. *General Construction in Steel – Code of Practice*. BIS.  
2. [Matplotlib Documentation](https://matplotlib.org)  
3. [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

---

## 🚀 Getting Started

### 🔄 Requirements

- Python 3.x
- PyQt5
- matplotlib

## 📄 License

This project is licensed under the MIT License.
