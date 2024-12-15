import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
from database import BibleReadingDB

# Inicializar banco de dados
db = BibleReadingDB()

def create_detailed_reading_plan():
    """
    Criar plano de leitura detalhado com todos os dias
    """
    reading_plan = {
        'Janeiro': {
            'Antigo Testamento': 'Gênesis 1-50',
            'Novo Testamento': 'Mateus 1-28',
            'Salmos': 'Salmos 1-31',
            'Provérbios': 'Provérbios 1-31',
            'Leitura Diária': {
                1: ['Gênesis 1-2', 'Mateus 1', 'Salmos 1', 'Provérbios 1'],
                2: ['Gênesis 3-4', 'Mateus 2', 'Salmos 2', 'Provérbios 2'],
                3: ['Gênesis 5-6', 'Mateus 3', 'Salmos 3', 'Provérbios 3'],
                # ... [Continuar com todos os dias]
            }
        },
        # ... [Adicionar todos os meses com detalhes diários]
    }
    return reading_plan

def main():
    st.title('Plano de Leitura Bíblica Anual')

    # Estilo CSS personalizado
    st.markdown("""
        <style>
        .stProgress > div > div > div > div {
            background-color: #4CAF50;
        }
        .big-font {
            font-size:20px !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    # Obter plano de leitura
    reading_plan = create_detailed_reading_plan()

    # Seleção do mês
    current_month = datetime.now().strftime('%B')
    selected_month = st.sidebar.selectbox(
        'Selecione o Mês',
        list(reading_plan.keys()),
        index=list(reading_plan.keys()).index(current_month) if current_month in reading_plan else 0
    )

    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["Visão Geral", "Leitura Diária", "Progresso"])

    # Carregar progresso do banco de dados
    saved_progress = db.get_progress(selected_month)

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Antigo Testamento')
            st.write(reading_plan[selected_month]['Antigo Testamento'])
            at_progress = st.slider(
                'Progresso Antigo Testamento',
                0, 100,
                value=saved_progress['AT'] if saved_progress else 0,
                key=f'at_{selected_month}'
            )

            st.subheader('Novo Testamento')
            st.write(reading_plan[selected_month]['Novo Testamento'])
            nt_progress = st.slider(
                'Progresso Novo Testamento',
                0, 100,
                value=saved_progress['NT'] if saved_progress else 0,
                key=f'nt_{selected_month}'
            )

        with col2:
            st.subheader('Salmos')
            st.write(reading_plan[selected_month]['Salmos'])
            salmos_progress = st.slider(
                'Progresso Salmos',
                0, 100,
                value=saved_progress['Salmos'] if saved_progress else 0,
                key=f'salmos_{selected_month}'
            )

            st.subheader('Provérbios')
            st.write(reading_plan[selected_month]['Provérbios'])
            prov_progress = st.slider(
                'Progresso Provérbios',
                0, 100,
                value=saved_progress['Proverbios'] if saved_progress else 0,
                key=f'prov_{selected_month}'
            )

    with tab2:
        st.subheader('Leitura Diária')
        day = st.selectbox('Selecione o dia', range(1, 32))
        if day in reading_plan[selected_month]['Leitura Diária']:
            daily_reading = reading_plan[selected_month]['Leitura Diária'][day]
            st.write(f"**Antigo Testamento:** {daily_reading[0]}")
            st.write(f"**Novo Testamento:** {daily_reading[1]}")
            st.write(f"**Salmos:** {daily_reading[2]}")
            st.write(f"**Provérbios:** {daily_reading[3]}")

            daily_completed = st.checkbox(
                'Marcar leitura como completa',
                value=saved_progress['Daily'] if saved_progress else False,
                key=f'complete_{selected_month}_{day}'
            )

    with tab3:
        total_progress = (at_progress + nt_progress + salmos_progress + prov_progress) / 4

        st.header('Progresso Geral do Mês')
        st.progress(total_progress / 100)
        st.markdown(f'<p class="big-font">Progresso Total: {total_progress:.1f}%</p>', unsafe_allow_html=True)

        st.header('Calendário de Leitura')
        month_num = list(calendar.month_name).index(selected_month)
        cal = calendar.monthcalendar(datetime.now().year, month_num)

        cal_df = pd.DataFrame(cal)
        cal_df.columns = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

        for week in cal:
            cols = st.columns(7)
            for idx, day in enumerate(week):
                if day != 0:
                    with cols[idx]:
                        st.checkbox(f'{day}', key=f'day_{selected_month}_{day}')

    # Botão para salvar progresso
    if st.button('Salvar Progresso'):
        db.save_progress(
            selected_month,
            at_progress,
            nt_progress,
            salmos_progress,
            prov_progress,
            daily_completed if 'daily_completed' in locals() else False
        )
        st.success('Progresso salvo com sucesso!')

if __name__ == '__main__':
    main()
