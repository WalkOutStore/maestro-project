from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import json
import os

from app.models.knowledge_base import KnowledgeRule
from app.schemas.knowledge_base import KnowledgeRuleCreate


class DynamicKnowledgeBase:
    """
    قاعدة المعرفة الديناميكية التي تخزن القواعد الرمزية وتتكيف مع البيانات الجديدة
    """
    
    def __init__(self, db: Session = None):
        """
        تهيئة قاعدة المعرفة
        """
        self.db = db
        self.rules_cache = {}
        self._load_rules()
    
    def _load_rules(self) -> None:
        """
        تحميل القواعد من قاعدة البيانات إلى الذاكرة المؤقتة
        """
        if self.db:
            rules = self.db.query(KnowledgeRule).filter(KnowledgeRule.is_active == True).order_by(KnowledgeRule.priority.desc()).all()
            for rule in rules:
                self.rules_cache[rule.id] = {
                    "name": rule.name,
                    "rule_type": rule.rule_type,
                    "conditions": rule.conditions,
                    "actions": rule.actions,
                    "priority": rule.priority
                }
    
    def add_rule(self, rule: KnowledgeRuleCreate) -> KnowledgeRule:
        """
        إضافة قاعدة جديدة إلى قاعدة المعرفة
        """
        if self.db:
            db_rule = KnowledgeRule(
                name=rule.name,
                description=rule.description,
                rule_type=rule.rule_type,
                conditions=rule.conditions,
                actions=rule.actions,
                priority=rule.priority,
                is_active=rule.is_active
            )
            self.db.add(db_rule)
            self.db.commit()
            self.db.refresh(db_rule)
            
            # تحديث الذاكرة المؤقتة
            self.rules_cache[db_rule.id] = {
                "name": db_rule.name,
                "rule_type": db_rule.rule_type,
                "conditions": db_rule.conditions,
                "actions": db_rule.actions,
                "priority": db_rule.priority
            }
            
            return db_rule
        return None
    
    def get_rules(self, rule_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        الحصول على القواعد من قاعدة المعرفة
        يمكن تصفية القواعد حسب النوع
        """
        rules = []
        for rule_id, rule_data in self.rules_cache.items():
            if rule_type is None or rule_data["rule_type"] == rule_type:
                rule_copy = rule_data.copy()
                rule_copy["id"] = rule_id
                rules.append(rule_copy)
        
        # ترتيب القواعد حسب الأولوية
        return sorted(rules, key=lambda x: x["priority"], reverse=True)
    
    def evaluate_rules(self, context: Dict[str, Any], rule_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        تقييم القواعد على سياق معين وإرجاع الإجراءات التي يجب اتخاذها
        """
        actions_to_take = []
        rules = self.get_rules(rule_type)
        
        for rule in rules:
            if self._evaluate_conditions(rule["conditions"], context):
                actions_to_take.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "actions": rule["actions"]
                })
        
        return actions_to_take
    
    def _evaluate_conditions(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        تقييم شروط القاعدة على سياق معين
        """
        # تنفيذ منطق تقييم الشروط هنا
        # هذا مثال بسيط، يمكن توسيعه حسب احتياجات المشروع
        
        if "operator" in conditions:
            operator = conditions["operator"]
            if operator == "AND":
                return all(self._evaluate_conditions(subcond, context) for subcond in conditions["conditions"])
            elif operator == "OR":
                return any(self._evaluate_conditions(subcond, context) for subcond in conditions["conditions"])
            elif operator == "NOT":
                return not self._evaluate_conditions(conditions["condition"], context)
        else:
            # شرط بسيط
            field = conditions.get("field")
            value = conditions.get("value")
            comparison = conditions.get("comparison", "eq")
            
            if field not in context:
                return False
            
            context_value = context[field]
            
            if comparison == "eq":
                return context_value == value
            elif comparison == "neq":
                return context_value != value
            elif comparison == "gt":
                return context_value > value
            elif comparison == "gte":
                return context_value >= value
            elif comparison == "lt":
                return context_value < value
            elif comparison == "lte":
                return context_value <= value
            elif comparison == "in":
                return context_value in value
            elif comparison == "contains":
                return value in context_value
        
        return False
    
    def update_from_feedback(self, rule_id: int, feedback: Dict[str, Any]) -> bool:
        """
        تحديث القاعدة بناءً على التغذية الراجعة
        """
        if self.db and rule_id in self.rules_cache:
            db_rule = self.db.query(KnowledgeRule).filter(KnowledgeRule.id == rule_id).first()
            if db_rule:
                # تنفيذ منطق تحديث القاعدة بناءً على التغذية الراجعة
                # هذا مثال بسيط، يمكن توسيعه حسب احتياجات المشروع
                
                # تحديث الأولوية بناءً على التغذية الراجعة
                if "is_useful" in feedback and feedback["is_useful"]:
                    db_rule.priority += 1
                else:
                    db_rule.priority = max(0, db_rule.priority - 1)
                
                # تحديث الشروط أو الإجراءات إذا لزم الأمر
                if "suggested_conditions" in feedback:
                    # دمج الشروط المقترحة مع الشروط الحالية
                    # هذا مثال بسيط، يمكن تنفيذ منطق أكثر تعقيدًا
                    db_rule.conditions.update(feedback["suggested_conditions"])
                
                if "suggested_actions" in feedback:
                    # دمج الإجراءات المقترحة مع الإجراءات الحالية
                    db_rule.actions.update(feedback["suggested_actions"])
                
                self.db.commit()
                
                # تحديث الذاكرة المؤقتة
                self.rules_cache[rule_id] = {
                    "name": db_rule.name,
                    "rule_type": db_rule.rule_type,
                    "conditions": db_rule.conditions,
                    "actions": db_rule.actions,
                    "priority": db_rule.priority
                }
                
                return True
        
        return False
    
    def export_rules(self, file_path: str) -> bool:
        """
        تصدير القواعد إلى ملف JSON
        """
        try:
            rules = self.get_rules()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(rules, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error exporting rules: {e}")
            return False
    
    def import_rules(self, file_path: str) -> bool:
        """
        استيراد القواعد من ملف JSON
        """
        if not os.path.exists(file_path):
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                rules = json.load(f)
            
            if self.db:
                for rule_data in rules:
                    # تجاهل معرف القاعدة عند الاستيراد
                    rule_id = rule_data.pop("id", None)
                    
                    # إنشاء كائن KnowledgeRuleCreate
                    rule = KnowledgeRuleCreate(
                        name=rule_data["name"],
                        rule_type=rule_data["rule_type"],
                        conditions=rule_data["conditions"],
                        actions=rule_data["actions"],
                        priority=rule_data["priority"],
                        is_active=True
                    )
                    
                    self.add_rule(rule)
                
                return True
        except Exception as e:
            print(f"Error importing rules: {e}")
        
        return False
