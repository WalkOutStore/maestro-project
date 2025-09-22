from typing import Dict, Any, List, Optional, Tuple
import json
import os
from sqlalchemy.orm import Session

from app.config import settings


class DataVisualizer:
    """
    مصور البيانات الذي يوفر تصورات مرئية للبيانات والتفسيرات
    """
    
    def __init__(self, db: Session = None):
        """
        تهيئة مصور البيانات
        """
        self.db = db
    
    def generate_visualization_config(self, data: Dict[str, Any], visualization_type: str) -> Dict[str, Any]:
        """
        توليد تكوين التصور المرئي بناءً على نوع التصور والبيانات
        """
        if visualization_type == "waterfall":
            return self._generate_waterfall_config(data)
        elif visualization_type == "bar":
            return self._generate_bar_config(data)
        elif visualization_type == "radar":
            return self._generate_radar_config(data)
        elif visualization_type == "line":
            return self._generate_line_config(data)
        elif visualization_type == "pie":
            return self._generate_pie_config(data)
        elif visualization_type == "sankey":
            return self._generate_sankey_config(data)
        else:
            # نوع تصور غير معروف، استخدام تكوين افتراضي
            return self._generate_default_config(data)
    
    def _generate_waterfall_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        توليد تكوين مخطط الشلال
        """
        factors = data.get("factors", [])
        importance = data.get("importance", [])
        descriptions = data.get("descriptions", [])
        
        # إنشاء بيانات المخطط
        chart_data = []
        
        # القيمة الأساسية
        base_value = 0
        chart_data.append({
            "name": "Base",
            "value": base_value,
            "itemStyle": {"color": "#91cc75"}
        })
        
        # إضافة العوامل
        for i, factor in enumerate(factors):
            value = importance[i] if i < len(importance) else 0
            description = descriptions[i] if i < len(descriptions) else ""
            
            chart_data.append({
                "name": factor,
                "value": value,
                "description": description,
                "itemStyle": {"color": "#5470c6" if value >= 0 else "#ee6666"}
            })
        
        # القيمة النهائية
        total_value = base_value + sum(importance)
        chart_data.append({
            "name": "Total",
            "value": total_value,
            "itemStyle": {"color": "#91cc75"}
        })
        
        # إنشاء تكوين المخطط
        config = {
            "title": {
                "text": data.get("title", "Factor Contribution"),
                "left": "center"
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": function_formatter
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "3%",
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": [item["name"] for item in chart_data],
                "axisLabel": {"rotate": 45}
            },
            "yAxis": {
                "type": "value"
            },
            "series": [
                {
                    "name": "Factor",
                    "type": "bar",
                    "stack": "total",
                    "label": {
                        "show": True,
                        "position": "top"
                    },
                    "data": chart_data
                }
            ]
        }
        
        return config
    
    def _generate_bar_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        توليد تكوين مخطط الأعمدة
        """
        factors = data.get("factors", [])
        importance = data.get("importance", [])
        descriptions = data.get("descriptions", [])
        
        # إنشاء بيانات المخطط
        chart_data = []
        for i, factor in enumerate(factors):
            value = importance[i] if i < len(importance) else 0
            description = descriptions[i] if i < len(descriptions) else ""
            
            chart_data.append({
                "name": factor,
                "value": value,
                "description": description
            })
        
        # ترتيب البيانات حسب القيمة
        chart_data.sort(key=lambda x: x["value"], reverse=True)
        
        # إنشاء تكوين المخطط
        config = {
            "title": {
                "text": data.get("title", "Factor Importance"),
                "left": "center"
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "formatter": function_formatter
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "3%",
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": [item["name"] for item in chart_data],
                "axisLabel": {"rotate": 45}
            },
            "yAxis": {
                "type": "value"
            },
            "series": [
                {
                    "name": "Importance",
                    "type": "bar",
                    "data": [{"value": item["value"], "description": item["description"]} for item in chart_data],
                    "itemStyle": {
                        "color": function_color_gradient
                    }
                }
            ]
        }
        
        return config
    
    def _generate_radar_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        توليد تكوين مخطط الرادار
        """
        factors = data.get("factors", [])
        importance = data.get("importance", [])
        
        # إنشاء تكوين المخطط
        config = {
            "title": {
                "text": data.get("title", "Factor Analysis"),
                "left": "center"
            },
            "tooltip": {},
            "radar": {
                "indicator": [{"name": factor, "max": 1} for factor in factors]
            },
            "series": [
                {
                    "name": "Factors",
                    "type": "radar",
                    "data": [
                        {
                            "value": importance,
                            "name": "Importance",
                            "areaStyle": {
                                "color": "rgba(84, 112, 198, 0.6)"
                            }
                        }
                    ]
                }
            ]
        }
        
        return config
    
    def _generate_line_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        توليد تكوين مخطط الخط
        """
        x_data = data.get("x_data", [])
        y_data = data.get("y_data", [])
        series_names = data.get("series_names", ["Series 1"])
        
        # إنشاء بيانات السلاسل
        series = []
        for i, name in enumerate(series_names):
            if i < len(y_data):
                series.append({
                    "name": name,
                    "type": "line",
                    "data": y_data[i]
                })
        
        # إنشاء تكوين المخطط
        config = {
            "title": {
                "text": data.get("title", "Trend Analysis"),
                "left": "center"
            },
            "tooltip": {
                "trigger": "axis"
            },
            "legend": {
                "data": series_names,
                "top": "bottom"
            },
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "10%",
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": x_data
            },
            "yAxis": {
                "type": "value"
            },
            "series": series
        }
        
        return config
    
    def _generate_pie_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        توليد تكوين مخطط الدائرة
        """
        factors = data.get("factors", [])
        importance = data.get("importance", [])
        
        # إنشاء بيانات المخطط
        chart_data = []
        for i, factor in enumerate(factors):
            if i < len(importance):
                chart_data.append({
                    "name": factor,
                    "value": importance[i]
                })
        
        # إنشاء تكوين المخطط
        config = {
            "title": {
                "text": data.get("title", "Distribution"),
                "left": "center"
            },
            "tooltip": {
                "trigger": "item",
                "formatter": "{a} <br/>{b}: {c} ({d}%)"
            },
            "legend": {
                "orient": "vertical",
                "left": "left",
                "data": factors
            },
            "series": [
                {
                    "name": "Distribution",
                    "type": "pie",
                    "radius": "50%",
                    "center": ["50%", "60%"],
                    "data": chart_data,
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)"
                        }
                    }
                }
            ]
        }
        
        return config
    
    def _generate_sankey_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        توليد تكوين مخطط سانكي
        """
        nodes = data.get("nodes", [])
        links = data.get("links", [])
        
        # إنشاء تكوين المخطط
        config = {
            "title": {
                "text": data.get("title", "Flow Diagram"),
                "left": "center"
            },
            "tooltip": {
                "trigger": "item",
                "triggerOn": "mousemove"
            },
            "series": [
                {
                    "type": "sankey",
                    "data": nodes,
                    "links": links,
                    "emphasis": {
                        "focus": "adjacency"
                    },
                    "lineStyle": {
                        "color": "gradient",
                        "curveness": 0.5
                    }
                }
            ]
        }
        
        return config
    
    def _generate_default_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        توليد تكوين افتراضي
        """
        # استخدام مخطط الأعمدة كتكوين افتراضي
        return self._generate_bar_config(data)
    
    def generate_decision_path_visualization(self, decision_path: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        توليد تصور مرئي لمسار القرار
        """
        # إنشاء العقد والروابط لمخطط سانكي
        nodes = []
        links = []
        
        # إضافة العقد
        for i, step in enumerate(decision_path):
            nodes.append({
                "name": step["name"]
            })
            
            # إضافة الروابط بين الخطوات
            if i > 0:
                links.append({
                    "source": decision_path[i-1]["name"],
                    "target": step["name"],
                    "value": step.get("weight", 1)
                })
            
            # إضافة الخيارات البديلة
            alternatives = step.get("alternatives", [])
            for alt in alternatives:
                nodes.append({
                    "name": alt["name"]
                })
                links.append({
                    "source": step["name"],
                    "target": alt["name"],
                    "value": alt.get("weight", 0.5)
                })
        
        # إنشاء بيانات التصور
        visualization_data = {
            "title": "Decision Path",
            "nodes": nodes,
            "links": links
        }
        
        # توليد تكوين مخطط سانكي
        return self._generate_sankey_config(visualization_data)
    
    def generate_comparison_visualization(self, scenarios: List[Dict[str, Any]], metrics: List[str]) -> Dict[str, Any]:
        """
        توليد تصور مرئي لمقارنة السيناريوهات
        """
        # استخراج أسماء السيناريوهات
        scenario_names = [scenario.get("description", f"Scenario {i+1}") for i, scenario in enumerate(scenarios)]
        
        # استخراج قيم المقاييس لكل سيناريو
        metric_values = []
        for metric in metrics:
            values = []
            for scenario in scenarios:
                values.append(scenario.get(metric, 0))
            metric_values.append(values)
        
        # إنشاء بيانات التصور
        visualization_data = {
            "title": "Scenario Comparison",
            "x_data": scenario_names,
            "y_data": metric_values,
            "series_names": metrics
        }
        
        # توليد تكوين مخطط الخط
        return self._generate_line_config(visualization_data)


# دوال مساعدة للتكوين

def function_formatter(params):
    """
    دالة لتنسيق التلميحات
    """
    return f"{params.seriesName}: {params.value} ({params.data.description if hasattr(params.data, 'description') else ''})"

def function_color_gradient(params):
    """
    دالة لإنشاء تدرج لوني
    """
    value = params.value
    if value >= 0.7:
        return "#5470c6"  # أزرق للقيم العالية
    elif value >= 0.4:
        return "#91cc75"  # أخضر للقيم المتوسطة
    else:
        return "#fac858"  # أصفر للقيم المنخفضة
