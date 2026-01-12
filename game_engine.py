from models import db, Country, EventLog
import random

class GameEngine:
    def execute_action(self, source_id, target_id, action_type, intensity, justification):
        """
        Eylemi gerçekleştirir ve ardından zincirleme reaksiyonları kontrol eder.
        """
        source = Country.query.get(source_id)
        target = Country.query.get(target_id)
        
        # --- [BURASI AYNI KALIYOR: Eylem Hesaplamaları] ---
        multiplier = 1.0
        if intensity == 'low': multiplier = 0.5
        elif intensity == 'high': multiplier = 1.5
        rng = random.uniform(0.9, 1.1)
        impact_report = []

        if action_type == "embargo":
            resource_loss = int(15 * multiplier * rng)
            target.oil -= resource_loss
            target.food -= int(resource_loss / 2)
            impact_report.append(f"Kaynaklar -{resource_loss}")
            inflation_spike = int(5 * multiplier * rng)
            target.inflation += inflation_spike
            impact_report.append(f"Enflasyon +%{inflation_spike}")
            target.budget -= int(target.budget * 0.05 * multiplier)
            source.budget -= int(source.budget * 0.01)

        elif action_type == "cyber_attack":
            tech_loss = int(12 * multiplier * rng)
            target.tech -= tech_loss
            impact_report.append(f"Teknoloji -{tech_loss}")
            happiness_loss = int(8 * multiplier * rng)
            target.happiness -= happiness_loss
            impact_report.append(f"Mutluluk -{happiness_loss}")
            target.budget -= int(target.budget * 0.03 * multiplier)

        elif action_type == "military_conflict":
            power_diff = (source.military - target.military) / 10
            base_damage = 10 * multiplier
            damage_target = int((base_damage + power_diff) * rng)
            target.military -= damage_target
            target.happiness -= int(10 * multiplier)
            target.budget -= 200
            impact_report.append(f"Hedef Askeri -{damage_target}")
            source.military -= int((base_damage - power_diff) * rng * 0.5) 
            source.oil -= int(10 * multiplier)
            source.budget -= 200

        elif action_type == "trade_deal":
            income = int(100 * multiplier * rng)
            source.budget += income
            target.budget += income
            source.inflation -= 1
            target.inflation -= 1
            impact_report.append(f"Gelir +${income}M")

        # --- SINIRLARI KORU (CLAMPING) ---
        self._clamp_values(source)
        self._clamp_values(target)

        # --- LOG VE KAYIT ---
        effects_str = ", ".join(impact_report)
        if justification:
            final_message = f"📢 {source.name} -> {target.name}: {justification} ({effects_str})"
        else:
            final_message = f"⚠️ {source.name}, {target.name} üzerinde {action_type} uyguladı. ({effects_str})"

        new_log = EventLog(message=final_message)
        db.session.add(new_log)
        
        # --- 🔥 KRİTİK NOKTA: OTOMATİK KRİZ KONTROLÜ ---
        # Eylem bitti, peki şimdi ülke ne durumda?
        trigger_message = self.check_triggers(target)
        
        # Eğer bir kriz tetiklendiyse onu da mesaja ekle
        if trigger_message:
            final_message += " || " + trigger_message

        db.session.commit()
        return final_message

    def check_triggers(self, country):
        """
        Ülkenin hayati değerlerini kontrol eder ve KRİZ senaryolarını tetikler.
        """
        triggered_events = []

        # 1. ENERJİ KRİZİ (Petrol < 10)
        if country.oil < 10:
            country.military -= 15     # Tanklar durdu
            country.budget -= int(country.budget * 0.10) # Fabrikalar durdu
            country.inflation += 10    # Enerji maliyeti fırladı
            triggered_events.append(f"🚨 ENERJİ KRİZİ! {country.name} karanlıkta. (Askeri -15, Enflasyon +10)")
        
        # 2. AÇLIK TEHLİKESİ (Gıda < 15)
        if country.food < 15:
            country.happiness -= 20    # Halk aç
            country.inflation += 15    # Gıda fiyatları uçtu
            triggered_events.append(f"🍞 AÇLIK TEHLİKESİ! {country.name} marketleri yağmalanıyor. (Mutluluk -20)")

        # 3. HİPERENFLASYON (Enflasyon > 40)
        if country.inflation > 40:
            country.budget -= int(country.budget * 0.20) # Para pul oldu
            country.happiness -= 15
            triggered_events.append(f"💸 HİPERENFLASYON! {country.name} ekonomisi çöküyor.")

        # 4. HÜKÜMET DÜŞMESİ (Mutluluk < 20)
        if country.happiness < 20:
            country.military -= 10 # Ordu bölünür
            triggered_events.append(f"🔥 İÇ SAVAŞ RİSKİ! {country.name} halkı sokaklara döküldü.")

        # Değerleri tekrar sınırla (Eksiye düşmesin)
        self._clamp_values(country)

        # Eğer bir olay tetiklendiyse veritabanına ayrıca haber olarak gir
        if triggered_events:
            full_msg = " | ".join(triggered_events)
            log = EventLog(message=full_msg)
            db.session.add(log)
            return full_msg
        
        return None

    def _clamp_values(self, country):
        """Değerleri 0-100 arasında tutan yardımcı fonksiyon"""
        country.military = max(0, min(100, country.military))
        country.oil = max(0, min(100, country.oil))
        country.food = max(0, min(100, country.food))
        country.tech = max(0, min(100, country.tech))
        country.happiness = max(0, min(100, country.happiness))
        country.inflation = max(0, country.inflation)