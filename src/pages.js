// Manifest of every static Stitch-exported screen, served from /public/pages/<slug>/index.html
export const pages = [
  { slug: "dashboard_overview", title: "Dashboard Overview", group: "Core" },
  { slug: "operational_reports_dashboard", title: "Operational Reports Dashboard", group: "Core" },
  { slug: "analysis_studio_populated_dashboard", title: "Analysis Studio", group: "Core" },
  { slug: "knowledge_base_portal", title: "Knowledge Base Portal", group: "Core" },

  { slug: "auth_portal_login_mode", title: "Login", group: "Auth & Onboarding" },
  { slug: "auth_portal_toggle_mode", title: "Login / Signup Toggle", group: "Auth & Onboarding" },
  { slug: "register_organization", title: "Register Organization", group: "Auth & Onboarding" },
  { slug: "registration_success_portal", title: "Registration Success", group: "Auth & Onboarding" },
  { slug: "industry_selection_portal", title: "Industry Selection", group: "Auth & Onboarding" },

  { slug: "ai_agents_workspace", title: "AI Agents Workspace", group: "Agents" },
  { slug: "ai_agent_conversation_portal", title: "Agent Conversation", group: "Agents" },
  { slug: "compliance_agent_chat_portal", title: "Compliance Agent Chat", group: "Agents" },
  { slug: "risk_predictor_chat_portal", title: "Risk Predictor Chat", group: "Agents" },
  { slug: "safety_monitor_chat_portal", title: "Safety Monitor Chat", group: "Agents" },
  { slug: "safety_monitor_chat_portal_dark_mode", title: "Safety Monitor Chat (Dark)", group: "Agents" },
  { slug: "document_analyzer_chat_portal", title: "Document Analyzer Chat", group: "Agents" },

  { slug: "security_audit_portal", title: "Security Audit", group: "Monitoring" },
  { slug: "log_auditor_agent_status", title: "Log Auditor Status", group: "Monitoring" },

  { slug: "users_management_portal", title: "Users Management", group: "Admin" },

  { slug: "integrated_ai_workspace_chemical_industry_1", title: "Integrated Workspace — Chemical (1)", group: "Industry Views" },
  { slug: "integrated_ai_workspace_chemical_industry_2", title: "Integrated Workspace — Chemical (2)", group: "Industry Views" },
  { slug: "sovereignx_landing_page_deep_obsidian_v2", title: "SovereignX Landing Page", group: "Industry Views" },
];
