import init
import streamlit as st
import pandas as pd

# טעינת הנתונים
df = init.init()

# סינון נתונים - הסרת שורות עם "טסט" בעמודת school
if 'school' in df.columns:
    df = df[df['school'] != 'טסט']

# הגדרת CSS עבור עיצוב משופר ונייד
st.markdown("""
<style>
/* עיצוב בסיסי */
.metric-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
}
.complete-record {
    background-color: #d4edda;
    color: #155724;
    padding: 0.2rem;
    border-radius: 0.3rem;
    font-weight: bold;
}
.partial-record {
    background-color: #f8d7da;
    color: #721c24;
    padding: 0.2rem;
    border-radius: 0.3rem;
    font-weight: bold;
}

/* עיצוב נייד */
@media (max-width: 768px) {
    .dataframe {
        font-size: 10px !important;
        overflow-x: auto;
    }
    
    .stDataFrame > div {
        overflow-x: auto;
    }
    
    .stDataFrame table {
        font-size: 10px !important;
    }
    
    h1, h2, h3 {
        font-size: 16px !important;
    }
    
    .stMetric {
        font-size: 12px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# יצירת טבלת מעקב עבור בתי ספר
st.title("📊 טבלת מעקב - מספר רשומות לפי בית ספר")

# יצירת טבלת ספירה עבור בתי הספר
if 'school' in df.columns:
    school_counts = df['school'].value_counts().reset_index()
    school_counts.columns = ['שם בית הספר', 'מספר רשומות']
    
    # הצגת טבלת המעקב לפי בית ספר
    # st.subheader("מעקב מילוי נתונים לפי בית ספר")
    # st.dataframe(school_counts, use_container_width=True, hide_index=True)    # יצירת טבלה משולבת לפי בית ספר וכיתה
    if 'class' in df.columns:
        st.subheader("📈 טבלת מעקב מפורטת - רשומות מלאות וחלקיות")
        
        # בדיקה אם קיימת עמודת conversation
        if 'conversation' in df.columns:            # יצירת עמודה חדשה לסוג הרשומה
            df['record_type'] = df['conversation'].apply(
                lambda x: 'מלא' if pd.notna(x) and str(x).strip() != '' else 'חלקי'
            )
              # יצירת טבלה משולבת עם פירוט לפי סוג רשומה
            detailed_counts = df.groupby(['school', 'class', 'record_type']).size().unstack(
                fill_value=0, level='record_type'
            )

            # שינוי שמות עמודות כיתות לתצוגה יותר ברורה
            detailed_counts.index = detailed_counts.index.set_names(['בית ספר', 'כיתה'])
            if 'class_8' in detailed_counts.index.get_level_values('כיתה'):
                detailed_counts = detailed_counts.rename(index={'class_8': 'כיתה ח'}, level='כיתה')
            if 'class_10' in detailed_counts.index.get_level_values('כיתה'):
                detailed_counts = detailed_counts.rename(index={'class_10': 'כיתה י'}, level='כיתה')              # אם אין עמודות מסוימות, נוסיף אותן עם ערכים של 0
            if 'מלא' not in detailed_counts.columns:
                detailed_counts['מלא'] = 0
            if 'חלקי' not in detailed_counts.columns:
                detailed_counts['חלקי'] = 0
              # סידור העמודות
            detailed_counts = detailed_counts[['מלא', 'חלקי']]
            
            # עיצוב הטבלה עם צבעים
            def style_dataframe(df):
                def color_cells(val):
                    if isinstance(val, (int, float)):
                        if val == 0:
                            return 'background-color: #f8f9fa; color: #6c757d;'
                        elif '✅' in str(df.columns[df.eq(val).any()].tolist()):
                            return 'background-color: #d4edda; color: #155724; font-weight: bold;'
                        elif '⚠️' in str(df.columns[df.eq(val).any()].tolist()):
                            return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
                        else:
                            return 'background-color: #e3f2fd; color: #0d47a1; font-weight: bold;'
                    return ''
                return df.style.applymap(color_cells)
              # הצגת הטבלה המפורטת
            st.dataframe(detailed_counts, use_container_width=True, hide_index=False)
              # יצירת טבלת סיכום לפי כיתות
            st.subheader("🎯 סיכום לפי כיתות")
            class_summary = df.groupby(['class', 'record_type']).size().unstack(
                fill_value=0, level='record_type'
            )
              # שינוי שמות כיתות לעברית
            class_summary.index = class_summary.index.str.replace('class_8', 'כיתה ח')
            class_summary.index = class_summary.index.str.replace('class_10', 'כיתה י')# אם אין עמודות מסוימות, נוסיף אותן עם ערכים של 0
            if 'מלא' not in class_summary.columns:
                class_summary['מלא'] = 0
            if 'חלקי' not in class_summary.columns:
                class_summary['חלקי'] = 0
                
            class_summary = class_summary[['מלא', 'חלקי']]
            
            st.dataframe(class_summary, use_container_width=True, hide_index=False)              # הוספת תובנות עם צבעים
            col1, col2 = st.columns(2)
            with col1:
                total_complete = df[df['record_type'] == 'מלא'].shape[0]
                st.success(f"✅ **רשומות מלאות**: {total_complete}")
            
            with col2:
                total_partial = df[df['record_type'] == 'חלקי'].shape[0]
                st.warning(f"⚠️ **רשומות חלקיות**: {total_partial}")
            
            # אחוז השלמה
            # completion_rate = (total_complete / len(df) * 100) if len(df) > 0 else 0
            # if completion_rate >= 75:
            #     st.success(f"🎉 **אחוז השלמה**: {completion_rate:.1f}% - מצוין!")
            # elif completion_rate >= 50:
            #     st.warning(f"📈 **אחוז השלמה**: {completion_rate:.1f}% - סביר")
            # else:
            #     st.error(f"📉 **אחוז השלמה**: {completion_rate:.1f}% - נדרש שיפור")
            
        else:
            st.warning("לא נמצאה עמודה בשם 'conversation' בנתונים - לא ניתן לחלק לרשומות מלאות וחלקיות")
              # הצגת טבלה רגילה אם אין עמודת conversation
            pivot_table = df.pivot_table(index='school', columns='class', aggfunc='size', fill_value=0)
            
            # שינוי שמות כיתות לעברית
            pivot_table.columns = pivot_table.columns.str.replace('class_8', 'כיתה ח')
            pivot_table.columns = pivot_table.columns.str.replace('class_10', 'כיתה י')
            
            st.dataframe(pivot_table, use_container_width=True, hide_index=False)
    else:
        st.warning("לא נמצאה עמודה בשם 'class' בנתונים - מציג רק לפי בית ספר")      # הצגת סיכום כללי
    st.subheader("📋 סיכום כללי")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🏫 סה\"כ בתי ספר", len(school_counts))
    
    with col2:
        st.metric("📚 סה\"כ רשומות", len(df))
    
else:
    st.error("לא נמצאה עמודה בשם 'school' בנתונים")

