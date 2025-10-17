import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# === Funções de cálculo ===

def calcular_custo_km(preco, consumo):
    return preco / consumo

def calcular_resultado(preco, tipo_consumo, valor, minimo=0, maximo=0):
    if tipo_consumo == "fixo":
        custo = calcular_custo_km(preco, valor)
        return (custo, custo), valor
    else:
        custo_min = calcular_custo_km(preco, maximo)
        custo_max = calcular_custo_km(preco, minimo)
        consumo_medio = (minimo + maximo) / 2
        return (custo_min, custo_max), consumo_medio

def comparar_combustivel(custo_etanol, custo_gasolina, consumo_et, consumo_gs, preco_etanol, preco_gasolina):
    et_min, et_max = custo_etanol
    gs_min, gs_max = custo_gasolina
    resultado = f"🚗 Etanol: R${et_min:.2f} a R${et_max:.2f}/km\n"
    resultado += f"⛽ Gasolina: R${gs_min:.2f} a R${gs_max:.2f}/km\n"

    if et_max < gs_min:
        resultado += "\n✅ Etanol é claramente mais vantajoso."
        limite = preco_etanol * (consumo_gs / consumo_et)
        resultado += f"\n💡 A gasolina só compensa se custar até R$ {limite:.2f}"
    elif gs_max < et_min:
        resultado += "\n✅ Gasolina é claramente mais vantajosa."
        limite = preco_gasolina * (consumo_et / consumo_gs)
        resultado += f"\n💡 O etanol só compensa se custar até R$ {limite:.2f}"
    else:
        resultado += "\n⚠️ Depende do cenário. Ambos podem ser vantajosos."
    return resultado

def mostrar_grafico_linha(custo_etanol, custo_gasolina, titulo="📊 Custo por Km"):
    x = ["Melhor Cenário", "Pior Cenário"]
    y_et = [custo_etanol[0], custo_etanol[1]]
    y_gs = [custo_gasolina[0], custo_gasolina[1]]

    plt.figure(figsize=(8, 5))
    plt.plot(x, y_et, marker='o', label='🚗 Etanol', color="green")
    plt.plot(x, y_gs, marker='s', label='⛽ Gasolina', color="orange")
    plt.title(titulo)
    plt.ylabel("Custo por Km (R$)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# === Cálculo principal ===

def calcular():
    try:
        preco_etanol = float(entry_preco_etanol.get())
        preco_gasolina = float(entry_preco_gasolina.get())
        trajeto = var_trajeto.get()
    except:
        messagebox.showerror("Erro", "Preencha os preços corretamente.")
        return

    trajetos = ["cidade", "estrada"] if trajeto == "ambos" else [trajeto]
    for t in trajetos:
        ce_tipo = consumo_vars[f"{t}_etanol"].get()
        cg_tipo = consumo_vars[f"{t}_gasolina"].get()

        try:
            if ce_tipo == "fixo":
                ce_valor = float(inputs[f"{t}_etanol_fixo"].get())
                custo_et, ce_media = calcular_resultado(preco_etanol, ce_tipo, ce_valor)
            else:
                ce_min = float(inputs[f"{t}_etanol_min"].get())
                ce_max = float(inputs[f"{t}_etanol_max"].get())
                custo_et, ce_media = calcular_resultado(preco_etanol, ce_tipo, 0, ce_min, ce_max)

            if cg_tipo == "fixo":
                cg_valor = float(inputs[f"{t}_gasolina_fixo"].get())
                custo_gs, cg_media = calcular_resultado(preco_gasolina, cg_tipo, cg_valor)
            else:
                cg_min = float(inputs[f"{t}_gasolina_min"].get())
                cg_max = float(inputs[f"{t}_gasolina_max"].get())
                custo_gs, cg_media = calcular_resultado(preco_gasolina, cg_tipo, 0, cg_min, cg_max)

        except:
            messagebox.showerror("Erro", f"Verifique os dados de consumo de {t}.")
            return

        resultado = comparar_combustivel(custo_et, custo_gs, ce_media, cg_media, preco_etanol, preco_gasolina)
        messagebox.showinfo(f"Resultado ({t.capitalize()})", resultado)
        mostrar_grafico_linha(custo_et, custo_gs, f"📊 Custo por Km - {t.capitalize()}")

# === Interface gráfica ===

root = tk.Tk()
root.title("Comparador de Etanol x Gasolina")
root.geometry("740x820")
root.resizable(False, False)

inputs = {}
consumo_vars = {}

tk.Label(root, text="Comparador de Combustível", font=("Arial", 16, "bold")).pack(pady=10)

# Preço
frame_precos = tk.Frame(root)
frame_precos.pack(pady=5)
tk.Label(frame_precos, text="Preço Etanol (R$):").grid(row=0, column=0)
entry_preco_etanol = tk.Entry(frame_precos)
entry_preco_etanol.grid(row=0, column=1, padx=10)
tk.Label(frame_precos, text="Preço Gasolina (R$):").grid(row=0, column=2)
entry_preco_gasolina = tk.Entry(frame_precos)
entry_preco_gasolina.grid(row=0, column=3, padx=10)

# Tipo de trajeto
frame_trajeto = tk.Frame(root)
frame_trajeto.pack(pady=5)
var_trajeto = tk.StringVar(value="ambos")
tk.Label(frame_trajeto, text="Tipo de trajeto:").pack(side="left")
tk.Radiobutton(frame_trajeto, text="Cidade", variable=var_trajeto, value="cidade").pack(side="left")
tk.Radiobutton(frame_trajeto, text="Estrada", variable=var_trajeto, value="estrada").pack(side="left")
tk.Radiobutton(frame_trajeto, text="Ambos", variable=var_trajeto, value="ambos").pack(side="left")

# Entradas de consumo
def criar_entrada_consumo(trajeto, combustivel):
    frame = tk.LabelFrame(root, text=f"{trajeto.capitalize()} - {combustivel.capitalize()}")
    frame.pack(padx=10, pady=5, fill="x")
    var_tipo = tk.StringVar(value="fixo")
    consumo_vars[f"{trajeto}_{combustivel}"] = var_tipo
    tk.Radiobutton(frame, text="Fixo", variable=var_tipo, value="fixo").pack(anchor="w")
    inputs[f"{trajeto}_{combustivel}_fixo"] = tk.Entry(frame)
    inputs[f"{trajeto}_{combustivel}_fixo"].pack(padx=10, fill="x")
    tk.Radiobutton(frame, text="Variação (mínimo e máximo)", variable=var_tipo, value="variacao").pack(anchor="w")
    subframe = tk.Frame(frame)
    subframe.pack()
    inputs[f"{trajeto}_{combustivel}_min"] = tk.Entry(subframe, width=10)
    inputs[f"{trajeto}_{combustivel}_min"].pack(side="left", padx=5)
    inputs[f"{trajeto}_{combustivel}_max"] = tk.Entry(subframe, width=10)
    inputs[f"{trajeto}_{combustivel}_max"].pack(side="left", padx=5)

for trajeto in ["cidade", "estrada"]:
    for combustivel in ["etanol", "gasolina"]:
        criar_entrada_consumo(trajeto, combustivel)

# Botão calcular
tk.Button(root, text="Calcular", command=calcular, bg="green", fg="white", width=25).pack(pady=20)

root.mainloop()
