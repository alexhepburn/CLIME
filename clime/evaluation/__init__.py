from .faithfulness import fidelity, local_fidelity, bal_fidelity, local_and_bal_fidelity
from .average_score import get_avg_score
from .key_points import get_key_points_score

AVAILABLE_EVALUATION_METRICS = {
    'fidelity (local)': local_fidelity,
    'fidelity (class balanced)': bal_fidelity,
    'fidelity (local and balanced)': local_and_bal_fidelity,
    'fidelity (normal)': fidelity,
}

AVAILABLE_EVALUATION_POINTS = {
    'all_test_points': get_key_points_score(key_points='all_points', test_points='all'),
    'class_means': get_key_points_score(key_points='means', test_points='all'),
    'between_class_means': get_key_points_score(key_points='between_means', test_points='all'),
    'all_test_points_local': get_key_points_score(key_points='all_points', test_points='local'),
    'class_means_local': get_key_points_score(key_points='means', test_points='local'),
    'between_class_means_local': get_key_points_score(key_points='between_means', test_points='local'),
}
