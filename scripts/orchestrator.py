import argparse
import os
import sys
import time

# Allow imports when run from project root or scripts/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
  sys.path.insert(0, SCRIPT_DIR)

from build_case_study import AnalyticsAgent, ReportAgent
from research_agent import ResearchAgent
from verify_results import VerificationAgent


class PipelineOrchestrator:
  """Central controller for the multi-stage research pipeline."""

  def __init__(self, base_dir=None):
    self.base_dir = base_dir or PROJECT_ROOT
    self.paths = {
      'json': os.path.join(self.base_dir, 'data', 'apps_research.json'),
      'csv': os.path.join(self.base_dir, 'data', 'apps_research.csv'),
      'verif': os.path.join(self.base_dir, 'data', 'verification_sample.csv'),
      'metrics': os.path.join(self.base_dir, 'data', 'verification_metrics.json'),
      'html': os.path.join(self.base_dir, 'public', 'index.html'),
    }

    self.research_agent = ResearchAgent(
      json_path=self.paths['json'],
      csv_path=self.paths['csv'],
    )
    self.verification_agent = VerificationAgent(
      verif_path=self.paths['verif'],
      metrics_path=self.paths['metrics'],
    )
    self.analytics_agent = AnalyticsAgent(
      json_path=self.paths['json'],
      metrics_path=self.paths['metrics'],
    )
    self.report_agent = ReportAgent(html_path=self.paths['html'])

  def run_research(self):
    print('\n[Orchestrator] Stage 1/3 — ResearchAgent: validating evidence links...')
    start = time.perf_counter()
    self.research_agent.audit()
    elapsed = time.perf_counter() - start
    print(f'[Orchestrator] Research stage completed in {elapsed:.2f}s')

  def run_verify(self):
    print('\n[Orchestrator] Stage 2/3 — VerificationAgent: computing QA metrics...')
    start = time.perf_counter()
    self.verification_agent.calculate_metrics()
    elapsed = time.perf_counter() - start
    print(f'[Orchestrator] Verification stage completed in {elapsed:.2f}s')

  def run_report(self):
    print('\n[Orchestrator] Stage 3/3 — AnalyticsAgent + ReportAgent: building dashboard...')
    start = time.perf_counter()
    agg = self.analytics_agent.aggregate()
    self.report_agent.write_report(agg)
    elapsed = time.perf_counter() - start
    print(f'[Orchestrator] Report stage completed in {elapsed:.2f}s')

  def run_all(self):
    print('=== PipelineOrchestrator: Starting full pipeline ===')
    pipeline_start = time.perf_counter()
    self.run_research()
    self.run_verify()
    self.run_report()
    elapsed = time.perf_counter() - pipeline_start
    print(f'\n=== PipelineOrchestrator: Pipeline complete in {elapsed:.2f}s ===')


def main():
  parser = argparse.ArgumentParser(description='Multi-stage OOP pipeline orchestrator')
  parser.add_argument('--run-all', action='store_true', help='Run research, verification, and report stages')
  parser.add_argument('--research', action='store_true', help='Run ResearchAgent link audit')
  parser.add_argument('--verify', action='store_true', help='Run VerificationAgent metrics')
  parser.add_argument('--report', action='store_true', help='Run AnalyticsAgent + ReportAgent dashboard build')
  args = parser.parse_args()

  orchestrator = PipelineOrchestrator()

  if args.run_all:
    orchestrator.run_all()
  elif args.research:
    orchestrator.run_research()
  elif args.verify:
    orchestrator.run_verify()
  elif args.report:
    orchestrator.run_report()
  else:
    parser.print_help()


if __name__ == '__main__':
  main()
