import os
import yaml
from typing import List, Set

class FeatureDisabler:
    """
    功能禁用管理类，处理YAML格式的禁用名单
    """
    def __init__(self):
        # 获取config目录路径
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.config_dir = os.path.join(self.base_dir, 'config')
        self.config_file = os.path.join(self.config_dir, 'disabled_features.yaml')
        
        # 确保config目录存在
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
        # 确保配置文件存在
        if not os.path.exists(self.config_file):
            self._save_disabled_features(set())
            
        self._disabled_features = self._load_disabled_features()
    
    def _load_disabled_features(self) -> Set[str]:
        """
        从YAML文件加载禁用的功能列表
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data and 'disabled_features' in data:
                    return set(data['disabled_features'])
        except Exception as e:
            print(f"加载禁用功能列表失败: {e}")
        return set()
    
    def _save_disabled_features(self, disabled_features: Set[str]) -> None:
        """
        将禁用的功能列表保存到YAML文件
        """
        try:
            # 确保config目录存在
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)
                
            data = {'disabled_features': list(disabled_features)}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        except Exception as e:
            print(f"保存禁用功能列表失败: {e}")
    
    def is_disabled(self, feature_name: str) -> bool:
        """
        检查功能是否被禁用
        """
        return feature_name in self._disabled_features
    
    def disable_feature(self, feature_name: str) -> bool:
        """
        禁用指定功能
        """
        if feature_name not in self._disabled_features:
            self._disabled_features.add(feature_name)
            self._save_disabled_features(self._disabled_features)
            return True
        return False
    
    def enable_feature(self, feature_name: str) -> bool:
        """
        启用指定功能
        """
        if feature_name in self._disabled_features:
            self._disabled_features.remove(feature_name)
            self._save_disabled_features(self._disabled_features)
            return True
        return False
    
    def get_disabled_features(self) -> List[str]:
        """
        获取所有被禁用的功能
        """
        return list(self._disabled_features)

# 创建全局实例
disabler = FeatureDisabler()

# 提供便捷函数
def is_disabled(feature_name: str) -> bool:
    return disabler.is_disabled(feature_name)

def disable_feature(feature_name: str) -> bool:
    return disabler.disable_feature(feature_name)

def enable_feature(feature_name: str) -> bool:
    return disabler.enable_feature(feature_name)

def get_disabled_features() -> List[str]:
    return disabler.get_disabled_features()