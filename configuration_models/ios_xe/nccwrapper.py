from time import sleep
from ncclient import manager
from ncclient.operations.rpc import RPCError
from xml.dom.minidom import parseString
import logging


class NccWrapper:

    def send_config(self, config, host, debug=False, max_retries=3, retry_interval=10):
        if debug:
            logger = logging.getLogger("ncclient")
            logger.setLevel(logging.DEBUG)

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            ch.setFormatter(formatter)

            logger.addHandler(ch)

        device = {
            "host": host,
            "port": 830,
            "username": "admin",
            "password": "admin",
            "device_params": {"name": "csr"},
            "hostkey_verify": False,
        }

        for attempt in range(max_retries):
            try:
                with manager.connect(**device) as conn:
                    out = conn.edit_config(target="candidate", config=config)
                    conn.commit()
                    logging.warning("Configuration sent successfully")
                    return out
            except RPCError as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    logging.info(f"Retrying in {retry_interval} seconds...")
                    sleep(retry_interval)
                else:
                    logging.error("All retries failed")
                    raise
