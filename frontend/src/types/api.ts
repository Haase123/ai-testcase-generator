export type Requirement = {
  id: number;
  title: string;
  description: string;
};

export type RequirementDetails = {
  id: number;
  title: string;
  description: string;
  generator_mode: "openai" | "rule-based";
  analysis: {
    priority: string;
    risk_level: string;
    quality_score: number;
    recommended_automation: string[];
  };
  test_cases: TestCases;
};

export type TestCases = {
  positive: string[];
  negative: string[];
  edge_cases: string[];
  security: string[];
};

export type Analysis = {
  priority: string;
  risk_level: string;
  quality_score: number;
  recommended_automation: string[];
};

export type ApiResponse = {
  id: number;
  requirement: string;
  generator_mode: "openai" | "rule-based";
  analysis: Analysis;
  test_cases: TestCases;
};

export type StatusResponse = {
  status: string;
  service: string;
  version: string;
  timestamp: string;
  services: {
    api: string;
    database: string;
    ai_generator: string;
    export: string;
  };
};