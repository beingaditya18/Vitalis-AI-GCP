import os
import google.generativeai as genai

class GeminiService:
    def __init__(self):
        api_key = os.environ.get('GEMINI_API_KEY')
        if api_key and api_key != 'your_gemini_api_key_here':
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def generate_clinical_summary(self, patient_text, structured_data=None):
        if not self.model:
            return "AI Summary unavailable (No API Key)"
        
        prompt = f"""
        You are an AI assistant for a doctor. Your task is to extract symptoms, 
        summarize the clinical history, and identify any red flags from the patient's input.
        DO NOT DIAGNOSE. DO NOT PRESCRIBE TREATMENT. Just summarize for the doctor.
        
        Patient Input: {patient_text}
        Structured Data: {structured_data}
        
        Format the output clearly with:
        - Symptoms Extracted
        - Clinical Summary
        - Potential Red Flags
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def generate_patient_safe_message(self, summary_text):
        if not self.model:
            return "Your consultation has been submitted to the doctor."

        prompt = f"""
        Given this clinical summary, generate a safe, reassuring, non-diagnostic message 
        to show the patient while they wait for the doctor. 
        DO NOT give medical advice.
        
        Clinical Summary: {summary_text}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Your consultation has been submitted. A doctor will review it shortly."

    def generate_doctor_explanation(self, summary_text, evidence_text):
        if not self.model:
            return "Explanation unavailable."

        prompt = f"""
        For the doctor, explain the reasoning behind the summary based on the evidence.
        Do not diagnose.
        
        Summary: {summary_text}
        Evidence: {evidence_text}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating explanation: {str(e)}"

gemini_service = GeminiService()
