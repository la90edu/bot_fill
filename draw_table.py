import init
import streamlit as st
import pandas as pd

# טעינת הנתונים
df = init.init()

# הגדרת layout רחב לשימוש טוב יותר במסך
# st.set_page_config(
#     layout="wide",
#     page_title="טבלת מעקב נתונים",
#     page_icon="📊"
# )

# סינון נתונים - הסרת שורות עם "טסט" בעמודת school
if 'school' in df.columns:
    df = df[df['school'] != 'טסט']

# הגדרת CSS עבור עיצוב משופר
st.markdown("""
<style>
/* עיצוב כללי */
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

/* עיצוב מותאם למובייל */
@media (max-width: 768px) {
    .stDataFrame {
        overflow-x: auto !important;
        width: 100% !important;
    }
    
    .stDataFrame > div {
        overflow-x: auto !important;
        white-space: nowrap !important;
    }
    
    /* הקטנת גופן בטבלאות במובייל */
    .stDataFrame table {
        font-size: 12px !important;
    }
    
    /* הקטנת כותרות */
    .stMarkdown h1 {
        font-size: 1.5rem !important;
    }
    
    .stMarkdown h2 {
        font-size: 1.3rem !important;
    }
    
    .stMarkdown h3 {
        font-size: 1.1rem !important;
    }
    
    /* שיפור תצוגת מטריקות במובייל */
    .metric-container {
        padding: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
}

/* כפיית גלילה אופקית לטבלאות */
.dataframe-container {
    overflow-x: auto;
    width: 100%;
}

/* סגנון מיוחד לטבלאות רחבות */
.wide-table {
    min-width: 600px;
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
        if 'conversation' in df.columns:
            # יצירת עמודה חדשה לסוג הרשומה
            df['record_type'] = df['conversation'].apply(
                lambda x: '✅ רשומה מלאה' if pd.notna(x) and str(x).strip() != '' else '⚠️ רשומה חלקית'
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
                detailed_counts = detailed_counts.rename(index={'class_10': 'כיתה י'}, level='כיתה')
            
            # אם אין עמודות מסוימות, נוסיף אותן עם ערכים של 0
            if '✅ רשומה מלאה' not in detailed_counts.columns:
                detailed_counts['✅ רשומה מלאה'] = 0
            if '⚠️ רשומה חלקית' not in detailed_counts.columns:
                detailed_counts['⚠️ רשומה חלקית'] = 0
              # סידור העמודות
            detailed_counts = detailed_counts[['✅ רשומה מלאה', '⚠️ רשומה חלקית']]
            
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
            st.dataframe(detailed_counts, use_container_width=True)
            
            # יצירת טבלת סיכום לפי כיתות
            st.subheader("🎯 סיכום לפי כיתות")
            class_summary = df.groupby(['class', 'record_type']).size().unstack(
                fill_value=0, level='record_type'
            )
              # אם אין עמודות מסוימות, נוסיף אותן עם ערכים של 0
            if '✅ רשומה מלאה' not in class_summary.columns:
                class_summary['✅ רשומה מלאה'] = 0
            if '⚠️ רשומה חלקית' not in class_summary.columns:
                class_summary['⚠️ רשומה חלקית'] = 0
                
            class_summary = class_summary[['✅ רשומה מלאה', '⚠️ רשומה חלקית']]
            
            st.dataframe(class_summary, use_container_width=True)
            
            # הוספת תובנות עם צבעים
            col1, col2 = st.columns(2)
            with col1:
                total_complete = df[df['record_type'] == '✅ רשומה מלאה'].shape[0]
                st.success(f"✅ **רשומות מלאות**: {total_complete}")
            
            with col2:
                total_partial = df[df['record_type'] == '⚠️ רשומה חלקית'].shape[0]
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
            st.dataframe(pivot_table, use_container_width=True)
    else:
        st.warning("לא נמצאה עמודה בשם 'class' בנתונים - מציג רק לפי בית ספר")
      # הצגת סיכום כללי
    st.subheader("📋 סיכום כללי")
    col1, col2  = st.columns(2             )
    
    with col1:
        st.metric("🏫 סה\"כ בתי ספר", len(school_counts))
    
    with col2:
        st.metric("📚 סה\"כ רשומות", len(df))
    

      # הצגת הנתונים המקוריים
    # st.subheader("טבלת הנתונים המלאה")
    # st.dataframe(df, use_container_width=True, hide_index=True)
    
else:
    st.error("לא נמצאה עמודה בשם 'school' בנתונים")
    st.subheader("טבלת הנתונים הזמינה")
    st.dataframe(df, use_container_width=True, hide_index=True)

