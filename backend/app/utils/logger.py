import logging

logging.basicConfig(
    filename="out.log",
    level=logging.INFO,
    format="%(asctime)s- %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)