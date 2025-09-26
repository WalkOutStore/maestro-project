from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import json
from datetime import datetime

from app.models.knowledge_base import KnowledgeRule
from app.schemas.knowledge_base import KnowledgeRuleCreate


class DynamicKnowledgeBase:
    """
    قاعدة المعرفة الديناميكية التي تعتمد على قواعد المخزنة في قاعدة البيانات
    والتغذية الراجعة من المستخدمين.
    """

    def __init__(self, db: Session = None):
        """
        تهيئة قاعدة المعرفة بدون أي قواعد افتراضية.
        """
        self.db = db
        self.rules_cache = {}
        self._load_rules()

    def _load_rules(self) -> None:
        """
        تحميل القواعد من قاعدة البيانات إلى الذاكرة المؤقتة
        """
        if self.db:
            rules = self.db.query(KnowledgeRule).filter(KnowledgeRule.is_active == True)\
                .order_by(KnowledgeRule.priority.desc()).all()
            for rule in rules:
                self.rules_cache[rule.id] = {
                    "name": rule.name,
                    "rule_type": rule.rule_type,
                    "conditions": json.loads(rule.conditions) if rule.conditions else {},
                    "actions": json.loads(rule.actions) if rule.actions else {},
                    "priority": rule.priority
                }

    def add_rule(self, rule: KnowledgeRuleCreate) -> Optional[KnowledgeRule]:
        """
        إضافة قاعدة جديدة إلى قاعدة المعرفة
        """
        if self.db:
            db_rule = KnowledgeRule(
                name=rule.name,
                description=rule.description,
                rule_type=rule.rule_type,
                conditions=json.dumps(rule.conditions) if isinstance(rule.conditions, dict) else rule.conditions,
                actions=json.dumps(rule.actions) if isinstance(rule.actions, dict) else rule.actions,
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
                "conditions": json.loads(db_rule.conditions) if db_rule.conditions else {},
                "actions": json.loads(db_rule.actions) if db_rule.actions else {},
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
        if not isinstance(conditions, dict):
            return False

        # التعامل مع الشرط البسيط
        if "field" in conditions and "value" in conditions:
            field = conditions["field"]
            value = conditions["value"]
            context_value = context.get(field)
            if isinstance(value, dict):
                # دعم بعض العمليات الشائعة مثل $gte, $lte
                for op, val in value.items():
                    if op == "$gte" and not (context_value >= val):
                        return False
                    if op == "$lte" and not (context_value <= val):
                        return False
            else:
                if context_value != value:
                    return False
            return True

        # التعامل مع الشروط المركبة
        if "operator" in conditions and "conditions" in conditions:
            operator = conditions["operator"].upper()
            sub_conditions = conditions["conditions"]
            if operator == "AND":
                return all(self._evaluate_conditions(sub, context) for sub in sub_conditions)
            elif operator == "OR":
                return any(self._evaluate_conditions(sub, context) for sub in sub_conditions)
            elif operator == "NOT":
                return not self._evaluate_conditions(sub_conditions[0], context) if sub_conditions else True

        return False

    def update_from_feedback(self, rule_id: int, feedback: Dict[str, Any]) -> bool:
        """
        تحديث القاعدة بناءً على التغذية الراجعة
        """
        if self.db and rule_id in self.rules_cache:
            db_rule = self.db.query(KnowledgeRule).filter(KnowledgeRule.id == rule_id).first()
            if db_rule:
                # تحديث الأولوية بناءً على التغذية الراجعة
                if feedback.get("is_useful", False):
                    db_rule.priority += 1
                else:
                    db_rule.priority = max(0, db_rule.priority - 1)

                # تحديث الشروط أو الإجراءات إذا لزم الأمر
                if "suggested_conditions" in feedback:
                    current_conditions = json.loads(db_rule.conditions) if db_rule.conditions else {}
                    current_conditions.update(feedback["suggested_conditions"])
                    db_rule.conditions = json.dumps(current_conditions)

                if "suggested_actions" in feedback:
                    current_actions = json.loads(db_rule.actions) if db_rule.actions else {}
                    current_actions.update(feedback["suggested_actions"])
                    db_rule.actions = json.dumps(current_actions)

                self.db.commit()

                # تحديث الذاكرة المؤقتة
                self.rules_cache[rule_id] = {
                    "name": db_rule.name,
                    "rule_type": db_rule.rule_type,
                    "conditions": json.loads(db_rule.conditions) if db_rule.conditions else {},
                    "actions": json.loads(db_rule.actions) if db_rule.actions else {},
                    "priority": db_rule.priority
                }
                return True
        return False

    def get_status(self) -> Dict[str, Any]:
        """
        الحصول على حالة قاعدة المعرفة
        """
        return {
            "rules_count": len(self.rules_cache),
            "active_rules": len([rule for rule in self.rules_cache.values() if rule.get("is_active", True)]),
            "rule_types": list(set(rule["rule_type"] for rule in self.rules_cache.values())),
            "last_updated": datetime.now().isoformat()
        }
