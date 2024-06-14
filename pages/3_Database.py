import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

import json

# Load the service account key from Streamlit secrets
try:
    key_dict = json.loads(st.secrets["textkey"])
except KeyError:
    st.error("Service account key not found in Streamlit secrets.")
    st.stop()

# Authenticate to Firestore with the JSON account key
try:
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="electricity-dashboard")
    st.success("Successfully authenticated to Firestore.")
except Exception as e:
    st.error(f"Failed to authenticate to Firestore: {e}")
    st.stop()
# Authenticate to Firestore with the JSON account key.

# Create a reference to the Google post.
doc_ref = db.collection("meters").document("meter_test")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())
st.write("Hello World")