import tkinter as tk
from tkinter import messagebox
import datetime

# === Funções de cálculo ===

def calcular_custo_km(preco, consumo):
    return preco / consumo

def calcular_resultado(preco, tipo_consumo, valor, minimo=0, maximo=0):
    if tipo_consumo == "fixo":
        custo = calcular_custo_km(preco, valor)
        return (custo, custo)
    else:
        custo_min = calcular_custo_km(preco, maximo)
        custo_max = calcular_custo_km(preco, minimo)
        return (custo_min, custo_max)

def comparar_combustivel(custo_etanol, custo_gasolina):
    et_min, et_max = custo_etanol
    gs_min, gs_max = custo_gasolina
    resultado = f"Etanol: R${et_min:.2f} a R${et_max:.2f}/km\n"
    resultado += f"Gasolina: R${gs_min:.2f} a R${gs_max:.2f}/km\n"
    if et_max < gs_min:
        resultado += "\n✅ Etanol é claramente mais vantajoso."
    elif gs_max < et_min:
        resultado += "\n✅ Gasolina é claramente mais vantajosa."
    else:
        resultado += "\n⚠️ Depende do cenário. Ambos podem ser vantajosos."
    return resultado

def sugestao_comb(preco_gasolina, consumo_etanol, consumo_gasolina):
    try:
        limite = preco_gasolina * (consumo_etanol / consumo_gasolina)
        return f"💡 Sugestão: o etanol só compensa se custar até R$ {limite:.2f} com esses consumos."
    except ZeroDivisionError:
        return "⚠️ Não foi possível calcular sugestão inteligente (divisão por zero)."

def mostrar_resultado(texto):
    def salvar_resultado_em_txt():
        agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"resultado_combustivel_{agora}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(texto)
        messagebox.showinfo("Salvo", f"Resultado salvo como:\n{nome_arquivo}")
    popup = tk.Toplevel(root)
    popup.title("Resultado da Comparação")
    popup.geometry("500x350")
    popup.resizable(False, False)
    resultado_box = tk.Text(popup, wrap="word", font=("Arial", 11))
    resultado_box.pack(padx=10, pady=10, fill="both", expand=True)
    resultado_box.insert("1.0", texto)
    resultado_box.config(state="disabled")
    frame_botoes = tk.Frame(popup)
    frame_botoes.pack(pady=5)
    tk.Button(frame_botoes, text="💾 Salvar Resultado", command=salvar_resultado_em_txt, bg="#808000", fg="white").pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Fechar", command=popup.destroy).pack(side="right", padx=10)

def abrir_calculo_reverso():
    def calcular_reverso():
        try:
            preco_et = float(entry_et.get())
            preco_gs = float(entry_gs.get())
            consumo_gs = float(entry_cg.get())
        except:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return
        trajeto = trajeto_var.get()
        resultado = ""
        if trajeto in ["cidade", "ambos"]:
            resultado += "🏙️ Cidade:\n"
            consumo_min_et_cidade = (preco_et / preco_gs) * consumo_gs
            resultado += f"➡️ O etanol só compensa se consumir pelo menos {consumo_min_et_cidade:.2f} km/l\n\n"
        if trajeto in ["estrada", "ambos"]:
            resultado += "🚗 Estrada:\n"
            consumo_min_et_estrada = (preco_et / preco_gs) * consumo_gs
            resultado += f"➡️ O etanol só compensa se consumir pelo menos {consumo_min_et_estrada:.2f} km/l"
        messagebox.showinfo("Resultado Reverso", resultado)
    popup = tk.Toplevel(root)
    popup.title("⛽ Cálculo Reverso")
    popup.geometry("300x350")
    popup.resizable(False, False)
    tk.Label(popup, text="Preço Etanol (R$):").pack()
    entry_et = tk.Entry(popup)
    entry_et.pack()
    tk.Label(popup, text="Preço Gasolina (R$):").pack()
    entry_gs = tk.Entry(popup)
    entry_gs.pack()
    tk.Label(popup, text="Consumo Gasolina (km/l):").pack()
    entry_cg = tk.Entry(popup)
    entry_cg.pack()
    trajeto_var = tk.StringVar(value="ambos")
    tk.Label(popup, text="\nTrajeto para análise:").pack()
    tk.Radiobutton(popup, text="Cidade", variable=trajeto_var, value="cidade").pack()
    tk.Radiobutton(popup, text="Estrada", variable=trajeto_var, value="estrada").pack()
    tk.Radiobutton(popup, text="Ambos", variable=trajeto_var, value="ambos").pack()
    tk.Button(popup, text="Calcular", command=calcular_reverso).pack(pady=10)

def limpar_campos():
    entry_preco_etanol.delete(0, tk.END)
    entry_preco_gasolina.delete(0, tk.END)
    var_trajeto.set("ambos")
    for entry in inputs.values():
        entry.delete(0, tk.END)
    for var in consumo_vars.values():
        var.set("fixo")

def get_consumo(trajeto, combustivel):
    tipo = consumo_vars[f"{trajeto}_{combustivel}"].get()
    try:
        if tipo == "fixo":
            valor = float(inputs[f"{trajeto}_{combustivel}_fixo"].get())
            return ("fixo", valor)
        else:
            minimo = float(inputs[f"{trajeto}_{combustivel}_min"].get())
            maximo = float(inputs[f"{trajeto}_{combustivel}_max"].get())
            return ("variacao", 0, minimo, maximo)
    except ValueError:
        messagebox.showerror("Erro", f"Consumo inválido para {combustivel} na {trajeto}.")
        return None

def calcular():
    try:
        preco_etanol = float(entry_preco_etanol.get())
        preco_gasolina = float(entry_preco_gasolina.get())
    except ValueError:
        messagebox.showerror("Erro", "Preencha corretamente os preços.")
        return
    resultados = []
    if var_trajeto.get() in ["cidade", "ambos"]:
        ce = get_consumo("cidade", "etanol")
        cg = get_consumo("cidade", "gasolina")
        if ce is None or cg is None: return
        custo_et = calcular_resultado(preco_etanol, *ce)
        custo_gs = calcular_resultado(preco_gasolina, *cg)
        resultado = comparar_combustivel(custo_et, custo_gs)
        if ce[0] == "fixo" and cg[0] == "fixo":
            resultado += "\n\n" + sugestao_comb(preco_gasolina, ce[1], cg[1])
        resultados.append("🏙️ CIDADE:\n" + resultado)
    if var_trajeto.get() in ["estrada", "ambos"]:
        ce = get_consumo("estrada", "etanol")
        cg = get_consumo("estrada", "gasolina")
        if ce is None or cg is None: return
        custo_et = calcular_resultado(preco_etanol, *ce)
        custo_gs = calcular_resultado(preco_gasolina, *cg)
        resultado = comparar_combustivel(custo_et, custo_gs)
        if ce[0] == "fixo" and cg[0] == "fixo":
            resultado += "\n\n" + sugestao_comb(preco_gasolina, ce[1], cg[1])
        resultados.append("🚗 ESTRADA:\n" + resultado)
    mostrar_resultado("\n\n".join(resultados))

# TELA
root = tk.Tk()
root.title("Comparador de Combustível")
root.geometry("740x820")
root.resizable(False, False)

inputs = {}
consumo_vars = {}

tk.Label(root, text="Comparador de Etanol x Gasolina", font=("Arial", 16, "bold")).pack(pady=10)

frame_precos = tk.Frame(root)
frame_precos.pack(pady=5)
tk.Label(frame_precos, text="Preço Etanol (R$):").grid(row=0, column=0)
tk.Label(frame_precos, text="Preço Gasolina (R$):").grid(row=0, column=2)
entry_preco_etanol = tk.Entry(frame_precos)
entry_preco_gasolina = tk.Entry(frame_precos)
entry_preco_etanol.grid(row=0, column=1, padx=10)
entry_preco_gasolina.grid(row=0, column=3, padx=10)

frame_trajeto = tk.Frame(root)
frame_trajeto.pack(pady=5)
var_trajeto = tk.StringVar(value="ambos")
tk.Label(frame_trajeto, text="Tipo de trajeto:").pack(side="left")
tk.Radiobutton(frame_trajeto, text="Cidade", variable=var_trajeto, value="cidade").pack(side="left")
tk.Radiobutton(frame_trajeto, text="Estrada", variable=var_trajeto, value="estrada").pack(side="left")
tk.Radiobutton(frame_trajeto, text="Ambos", variable=var_trajeto, value="ambos").pack(side="left")

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

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=15)
tk.Button(frame_botoes, text="Calcular", command=calcular, bg="green", fg="white", width=20).pack(pady=5)
tk.Button(frame_botoes, text="Novo Cálculo", command=limpar_campos, bg="#4682b4", fg="white", width=20).pack(pady=5)
tk.Button(frame_botoes, text="⛽ Cálculo Reverso", command=abrir_calculo_reverso, bg="#ff8c00", fg="white", width=20).pack(pady=5)

root.mainloop()