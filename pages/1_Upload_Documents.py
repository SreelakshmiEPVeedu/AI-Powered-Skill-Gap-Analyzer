# pages/1_Upload_Documents.py
import streamlit as st
from backend.document_processor import DocumentProcessor
from helpers import initialize_session_state

# Initialize session state and components
initialize_session_state()

def main():
    st.markdown('<h2 class="sub-header">📁 Upload Documents</h2>', unsafe_allow_html=True)
    
    document_processor = DocumentProcessor()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Upload Resume")
        resume_file = st.file_uploader("Choose a resume file", type=['pdf', 'docx', 'txt'], key="resume")
        
        if resume_file is not None:
            with st.spinner("Processing resume..."):
                result = document_processor.process_uploaded_file(resume_file)
                
                if result["success"]:
                    st.session_state.resume_data = result
                    st.success("✅ Resume processed successfully!")
                else:
                    st.error(f"❌ Error processing resume: {result['error']}")
    
    with col2:
        st.subheader("📝 Paste Job Description")
        job_desc_text_input = st.text_area("Paste the job description here", height=200, key="job_desc_text")
        if st.button("Use Pasted Job Description", key="use_job_desc_text"):
            if job_desc_text_input.strip():
                processed_text = document_processor.preprocess_text(job_desc_text_input)
                st.session_state.job_desc_data = {
                    "success": True,
                    "text": processed_text,
                    "file_type": "text/plain",
                    "file_name": "pasted_job_desc.txt"
                }
                st.success("✅ Job description text saved successfully!")
            else:
                st.warning("Please enter some job description text.")
    
    # Status indicator
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.resume_data:
            st.success("✅ Resume: Ready")
        else:
            st.warning("⚠️ Resume: Not uploaded")
    
    with col2:
        if st.session_state.job_desc_data:
            st.success("✅ Job Description: Ready")
        else:
            st.warning("⚠️ Job Description: Not uploaded")
    
    # Navigation hint
    if st.session_state.resume_data and st.session_state.job_desc_data:
        st.markdown("---")
        st.success("🎉 Documents ready! Proceed to **Skill Analysis** to run the analysis.")

if __name__ == "__main__":
    main()
