#!/bin/bash
# hive-builder にパッチを当てます。hive-builder-templateが形になった段階で 製品の方にマージします。
sudo find $(hive get-install-dir) -type f -exec sed -i 's/\/usr\/bin\/env python/\/usr\/bin\/python/g' {} \;