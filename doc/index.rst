===========================
Sphinx ER Diagram Extention
===========================

| sphinx_erdiagramはER図を描くためのSphinx拡張です。
| **er-diagram**\ ディレクティブを利用してER図を描けます。

.. code-block:: rst

    .. er-diagram::

       entities:
         エンティティ1:
           columns:
             - 項目1: { label: string, pk: true, notnull: true }
             - 項目2
         エンティティ2:
           columns:
             - 項目1: { label: string, pk: true, notnull: true }
             - 項目2
         エンティティ3:
           columns:
             - 項目1
             - 項目2

       relations:
         - エンティティ1 -- エンティティ2
         - エンティティ2 -> エンティティ3

.. er-diagram::

    entities:
      エンティティ1:
        columns:
          - 項目1: { label: string, pk: true, notnull: true }
          - 項目2
      エンティティ2:
        columns:
          - 項目1: { label: string, pk: true, notnull: true }
          - 項目2
      エンティティ3:
        columns:
          - 項目1
          - 項目2

    relations:
      - エンティティ1 -- エンティティ2
      - エンティティ2 -> エンティティ3

Contents
===========

.. toctree::
   :maxdepth: 1
   :numbered:
   :glob:

   settings
   writingstyle


.. include:: ../CHANGES.rst

License
========

.. include:: ../LICENSE
   :literal: