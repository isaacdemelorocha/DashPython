import streamlit as st
import pandas as pd
import plotly.express as px
import tempfile


# Função para fazer upload do arquivo Excel
def upload_file():
    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])
    return uploaded_file


# Função para exibir dados do arquivo Excel
def display_excel_data(df):
    st.write("**Dados do Arquivo Excel**")
    st.dataframe(df)


# Função para criar gráfico de linha interativo com Plotly
def create_line_chart(df, x_column, y_column, status_column):
    fig = px.line(df, x=x_column, y=y_column, color=status_column,
                  title=f"{y_column} ao Longo de {x_column}", line_shape='linear', markers=True,
                  template="plotly", color_discrete_sequence=px.colors.qualitative.Set1)  # Definir a paleta de cores
    return fig


# Função para criar gráfico de barras interativo com Plotly
def create_bar_chart(df, x_column, y_column, status_column):
    fig = px.bar(df, x=x_column, y=y_column, color=status_column,
                 title=f"{y_column} por {x_column}",
                 color_discrete_sequence=px.colors.qualitative.Set1)  # Definir a paleta de cores
    return fig


# Função para criar gráfico de dispersão interativo com Plotly
def create_scatter_chart(df, x_column, y_column, status_column):
    fig = px.scatter(df, x=x_column, y=y_column, color=status_column,
                     title=f"Dispersão entre {x_column} e {y_column}",
                     color_discrete_sequence=px.colors.qualitative.Set1)  # Definir a paleta de cores
    return fig


# Função para criar gráfico de pizza interativo com Plotly
def create_pie_chart(df, column, status_column):
    fig = px.pie(df, names=column, title=f"Distribuição de {column}",
                 color=status_column,
                 color_discrete_sequence=px.colors.qualitative.Set1)  # Definir a paleta de cores
    return fig


# Função para criar boxplot com Plotly
def create_boxplot(df, x_column, y_column, status_column):
    fig = px.box(df, x=x_column, y=y_column, color=status_column,
                 title=f"Boxplot de {y_column} por {x_column}",
                 color_discrete_sequence=px.colors.qualitative.Set1)  # Definir a paleta de cores
    return fig


# Função para salvar o gráfico Plotly como imagem (PNG, JPG, SVG)
def save_plotly_as_image(fig, file_format="png"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_format}") as tmpfile:
        img_path = tmpfile.name
        fig.write_image(img_path, format=file_format)
    return img_path


# Função principal do app
def main():
    st.title("Dashboard Interativo")

    # Etapa 1: Upload de arquivo Excel
    uploaded_file = upload_file()

    if uploaded_file is not None:
        # Etapa 2: Ler o arquivo Excel
        df = pd.read_excel(uploaded_file)

        # Exibir os dados
        display_excel_data(df)

        # Etapa 3: Opções para criar gráficos
        st.sidebar.header("Personalização do Dashboard")

        # Seleção de colunas para os gráficos
        columns = df.columns.tolist()

        # Adiciona a opção para adicionar múltiplos gráficos
        num_graphs = st.sidebar.number_input("Quantos gráficos você deseja adicionar?", min_value=1, max_value=5,
                                             value=1)

        # Armazena os gráficos gerados
        generated_figures = []

        for i in range(num_graphs):
            chart_type = st.sidebar.selectbox(f"Selecione o tipo de gráfico #{i + 1}",
                                              ["Gráfico de Linha", "Gráfico de Barras", "Gráfico de Dispersão",
                                               "Gráfico de Pizza", "Boxplot"], key=f"chart_type_{i}")

            # Substituição do texto explicativo
            status_column = st.sidebar.selectbox(
                f"Selecione a coluna que deseja usar para colorir o gráfico #{i + 1} e diferenciar as categorias",
                columns, key=f"status_column_{i}")

            # Condicional para criar gráficos com base na seleção
            if chart_type == "Gráfico de Linha":
                x_column = st.sidebar.selectbox(f"Selecione a coluna do eixo X para o gráfico #{i + 1}", columns,
                                                key=f"x_column_{i}")
                y_column = st.sidebar.selectbox(f"Selecione a coluna do eixo Y para o gráfico #{i + 1}", columns,
                                                key=f"y_column_{i}")
                fig = create_line_chart(df, x_column, y_column, status_column)

            elif chart_type == "Gráfico de Barras":
                x_column = st.sidebar.selectbox(f"Selecione a coluna do eixo X para o gráfico #{i + 1}", columns,
                                                key=f"x_column_{i}")
                y_column = st.sidebar.selectbox(f"Selecione a coluna do eixo Y para o gráfico #{i + 1}", columns,
                                                key=f"y_column_{i}")
                fig = create_bar_chart(df, x_column, y_column, status_column)

            elif chart_type == "Gráfico de Dispersão":
                x_column = st.sidebar.selectbox(f"Selecione a coluna do eixo X para o gráfico #{i + 1}", columns,
                                                key=f"x_column_{i}")
                y_column = st.sidebar.selectbox(f"Selecione a coluna do eixo Y para o gráfico #{i + 1}", columns,
                                                key=f"y_column_{i}")
                fig = create_scatter_chart(df, x_column, y_column, status_column)

            elif chart_type == "Gráfico de Pizza":
                column = st.sidebar.selectbox(f"Selecione a coluna para o gráfico de pizza #{i + 1}", columns,
                                              key=f"column_{i}")
                fig = create_pie_chart(df, column, status_column)

            elif chart_type == "Boxplot":
                x_column = st.sidebar.selectbox(f"Selecione a coluna do eixo X para o gráfico #{i + 1}", columns,
                                                key=f"x_column_{i}")
                y_column = st.sidebar.selectbox(f"Selecione a coluna do eixo Y para o gráfico #{i + 1}", columns,
                                                key=f"y_column_{i}")
                fig = create_boxplot(df, x_column, y_column, status_column)

            # Exibe o gráfico gerado
            st.plotly_chart(fig)

            # Detalhamento da quantidade
            status_counts = df[status_column].value_counts()

            # Exibindo informações detalhadas
            st.write(f"**Total de entradas:** {len(df)}")
            st.write(f"**Quantidade de valores únicos na coluna '{status_column}':**")

            # Exibindo as categorias com suas contagens
            for category, count in status_counts.items():
                st.write(f"- {category}: {count}")

            # Salvar os gráficos gerados
            img_path = save_plotly_as_image(fig, file_format="png")
            generated_figures.append((img_path, f"Gráfico #{i + 1} - {chart_type}"))


if __name__ == "__main__":
    main()
