const API_URL = "http://127.0.0.1:8000";


// =====================================================
// BACKEND TEST
// =====================================================

export async function testBackend() {
  const response = await fetch(`${API_URL}/`);

  if (!response.ok) {
    throw new Error("Backend connection failed");
  }

  return await response.json();
}


// =====================================================
// DATABASE TEST
// =====================================================

export async function testDatabase() {
  const response = await fetch(`${API_URL}/db-test`);

  if (!response.ok) {
    throw new Error("Database connection failed");
  }

  return await response.json();
}


// =====================================================
// WORKSPACE
// =====================================================

export async function createWorkspace(name, industry) {

  const response = await fetch(
    `${API_URL}/workspaces/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        name,
        industry,
      }),
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Failed to create workspace"
    );
  }

  return await response.json();
}


export async function getWorkspaces() {

  const response = await fetch(
    `${API_URL}/workspaces/`
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Failed to get workspaces"
    );
  }

  return await response.json();
}


export async function getWorkspace(workspaceId) {

  const response = await fetch(
    `${API_URL}/workspaces/${workspaceId}`
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Failed to get workspace"
    );
  }

  return await response.json();
}


export async function updateWorkspace(
  workspaceId,
  name,
  industry
) {

  const response = await fetch(
    `${API_URL}/workspaces/${workspaceId}`,
    {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        name,
        industry,
      }),
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Failed to update workspace"
    );
  }

  return await response.json();
}


export async function deleteWorkspace(workspaceId) {

  const response = await fetch(
    `${API_URL}/workspaces/${workspaceId}`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Failed to delete workspace"
    );
  }

  return await response.json();
}


// =====================================================
// DOCUMENTS
// =====================================================

export async function uploadDocument(
  workspaceId,
  file
) {

  const formData = new FormData();

  formData.append(
    "workspace_id",
    workspaceId
  );

  formData.append(
    "file",
    file
  );

  const response = await fetch(
    `${API_URL}/documents/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Document upload failed"
    );
  }

  return await response.json();
}


export async function getDocuments(
  workspaceId
) {

  const response = await fetch(
    `${API_URL}/documents/${workspaceId}`
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Failed to get documents"
    );
  }

  return await response.json();
}


export async function previewDocument(
  documentId
) {

  const response = await fetch(
    `${API_URL}/documents/preview/${documentId}`
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Preview failed"
    );
  }

  return await response.json();
}


export async function updateDocument(
  documentId,
  data
) {

  const response = await fetch(
    `${API_URL}/documents/${documentId}`,
    {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Failed to update document"
    );
  }

  return await response.json();
}


export async function deleteDocument(
  documentId
) {

  const response = await fetch(
    `${API_URL}/documents/${documentId}`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Failed to delete document"
    );
  }

  return await response.json();
}


// =====================================================
// AI ANALYSIS
// =====================================================

export async function startAnalysis(
  documentId,
  analysisType = "full"
) {

  const response = await fetch(
    `${API_URL}/analysis/${documentId}`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        analysis_type: analysisType,
      }),
    }
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "AI analysis failed"
    );
  }

  return await response.json();
}


export async function getAnalysis(
  documentId
) {

  const response = await fetch(
    `${API_URL}/analysis/${documentId}`
  );

  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Analysis result not found"
    );
  }

  return await response.json();
}