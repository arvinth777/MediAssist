# Example Queries for MediAssist RAG

Test the system with these sample questions about maternal health:

## Complications & Risks

1. **"What are complications of gestational diabetes?"**
   - Tests retrieval from GDM complications document

2. **"What are risk factors for preeclampsia?"**
   - Tests retrieval from preeclampsia risk document

3. **"What causes postpartum hemorrhage?"**
   - Tests retrieval from PPH document

4. **"Signs of preterm birth?"**
   - Tests retrieval from preterm birth risk document

## Screening & Diagnosis

5. **"How is anemia in pregnancy diagnosed?"**
   - Tests retrieval from anemia pregnancy document

6. **"What ultrasound measurements are taken during pregnancy?"**
   - Tests retrieval from fetal ultrasound markers document

7. **"What is fetal growth restriction?"**
   - Tests retrieval from FGR document

## Management & Treatment

8. **"How is anemia in pregnancy treated?"**
   - Tests retrieval from anemia pregnancy document

9. **"What are components of antenatal care?"**
   - Tests retrieval from antenatal care basics document

10. **"What infections are screened in pregnancy?"**
    - Tests retrieval from maternal infections document

## Complex Queries

11. **"Compare hypertensive disorders of pregnancy"**
    - Tests retrieval across hypertensive disorders document

12. **"What are long-term risks after gestational diabetes?"**
    - Tests understanding of GDM complications

13. **"Prevention of preeclampsia"**
    - Tests retrieval from preeclampsia risk document

14. **"Management of severe postpartum hemorrhage"**
    - Tests retrieval from PPH document

15. **"Difference between chronic and gestational hypertension"**
    - Tests retrieval from hypertensive disorders document

## Expected Behavior

- **Fast app (app_fast.py)**: Shows top 3 retrieved document chunks instantly
- **Full app (app.py)**: Generates a synthesized answer with citations [1], [2], [3]

## Tips

- Be specific in your questions
- The system only knows what's in the 10 corpus documents
- Answers should cite sources using [1]/[2]/[3] notation
- Medical advice disclaimer applies - this is educational only
