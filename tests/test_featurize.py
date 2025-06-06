import pytest
from src.featurize_cifs import batch_featurize_cifs_parallel

def test_featurize_runs():
    # Run featurization on a small sample folder (adjust paths accordingly)
    try:
        batch_featurize_cifs_parallel('data/raw/sample_cifs', 'results/features/test_features.csv', 'results/logs/test_featurization.log', workers=1)
    except Exception as e:
        pytest.fail(f"Featurization failed with error: {e}")

