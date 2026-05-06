# HLA Eplet Analyzer

This web application provides both a browser interface and a web service for predicting anti-HLA antibody targets at the eplet level using machine learning.

## Validation

The datasets comprise mismatched eplets from HLA alleles tested on single-antigen bead panels. The experiments evaluate the classification of each eplet–panel pair into low- and high-reactivity categories. All validation files are at the [validation](https://github.com/mariomarroquim/hla-eplet-analyzer/tree/main/validation) folder.

* Basic validation: 89% accuracy and 88% AUC-ROC.
* Regular cross-validation: 88% accuracy and 92% AUC-ROC.
* Cross-validation with feature selection: 89% accuracy and 94% AUC-ROC.
* Cross-validation with feature selection and hyperparameter tuning: 91% accuracy and 94% AUC-ROC.

## Instructions

This is a standard Python application. Run `sh run_development.sh`, then open [http://localhost:5000](http://localhost:5000).

## Support

You can contact me at mariomarroquim@gmail.com.
