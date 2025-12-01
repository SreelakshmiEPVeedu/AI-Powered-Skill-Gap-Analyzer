# pages/1_Upload_Documents.py
 
import streamlit as st    #for frontend
from backend.document_processor import DocumentProcessor  #for processing the document
from helpers import initialize_session_state   #for real time data
def main():
    with st.sidebar:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_id = None    
            st.rerun()
    st.markdown('<h2 class="sub-header">📁 Upload Documents</h2>', unsafe_allow_html=True)
    document_processor = DocumentProcessor()
    col1, col2 = st.columns(2)
    #uploads resume
    with col1:
        st.subheader("📄 Upload Resume")
        resume_file = st.file_uploader("Choose a resume file", type=['pdf', 'docx', 'txt'])
        
        if resume_file is not None:
            with st.spinner("Processing resume..."):
                #function to upload resume
                result = document_processor.process_uploaded_file(resume_file) 
                
                if result["success"]:
                    st.session_state.resume_data = result
                    st.success("✅ Resume processed successfully!")
                else:
                    st.error(f"❌ Error processing resume")
    
    with col2:
        st.subheader("📝 Paste Job Description")
        job_desc_text_input = st.text_area("Paste the job description here", height=200)
        if st.button("Use Pasted Job Description", key="use_job_desc_text"):
            if job_desc_text_input.strip():
                #processes text
                processed_text = document_processor.preprocess_text(job_desc_text_input)
                st.session_state.job_desc_data = {
                    "success": True,
                    "text": processed_text
                }
                st.success("✅ Job description text saved successfully!")
            else:
                st.warning("Please enter some job description text.")
    st.markdown("---")
    # Navigation hint
    if st.session_state.resume_data and st.session_state.job_desc_data:
        st.markdown("---")
        st.success("🎉 Documents ready! Proceed to **Skill Analysis** to run the analysis.")

if __name__ == "__main__":
    main()
