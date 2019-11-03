const assert = require('power-assert');
const chrome = require('selenium-webdriver/chrome');
const {Builder, By, Key, until} = require('selenium-webdriver');

class FishesList {

  constructor(driver) {
    this.driver = driver;
  }

  async open() {
    await this.driver.get('http://localhost:8080');
    return this;
  }

  async waitForRowToFinishLoading() {
    await this.driver.wait(async () => {
      const rows = await this.getRows();
      return rows.length !== 0;
    }, 5000);
    return this;
  }

  async clickSelect() {
    await this.driver.findElement(By.id('select-button')).click();
    return this.driver.switchTo().alert();
  }

  async clickAllCheck() {
    const check = await this.driver.findElement(By.id('all-check'));
    check.click();
    return this;
  }

  async getRows() {
    const rows = await this.driver.findElement(By.id('fishes-list')).findElements(By.tagName('tr'));
    return rows.map(r => {
      return new FishesListRow(this.driver, r);
    });
  }
}

class FishesListRow {

  constructor(driver, el) {
    this._driver = driver;
    this._el = el;
  }

  async getName() {
    const cols = await this._el.findElements(By.tagName('td'));
    return cols[1].getText();
  }

  async clickCheckBox() {
    await this._el.findElement(By.className('select-row')).click();
    return this;
  }

}

describe('FishList', function() {

  this.timeout(20000);

  let driver;

  beforeEach(() => {
    driver = new Builder()
      .forBrowser('chrome')
      .setChromeOptions(new chrome.Options().headless())
      .build();
  });

  afterEach(() => {
    return driver.quit();
  });

  it('一覧が動的に読み込まれること', async () => {
    const p = new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const rows = await p.getRows();

    assert(rows.length === 3);

    assert(await rows[0].getName() === 'まぐろ')
    assert(await rows[1].getName() === 'はまち')
    assert(await rows[2].getName() === 'かつお')
  });

  it('未選択状態で"けってい"するとアラートがでること', async () => {
    const p =  new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const alert = await p.clickSelect();
    assert(await alert.getText() === 'せんたくしてください');
  });

  it('一覧のアイテムを1件選択して"けってい"すると選択結果が表示されること', async () => {
    const p =  new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const rows = await p.getRows();
    await rows[0].clickCheckBox(0);

    const alert = await p.clickSelect();
    assert(await alert.getText() === 'まぐろ');
  });

  it('一覧のアイテムを複数件選択して"けってい"すると選択結果が表示されること', async () => {
    const p =  new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const rows = await p.getRows();
    await rows[1].clickCheckBox();
    await rows[0].clickCheckBox();

    const alert = await p.clickSelect();
    assert(await alert.getText() === 'まぐろ,はまち');
  });

  it('全体チェックをするとすべてのアイテムが選択されること', async () => {
    const p =  new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const rows = await p.getRows();
    await rows[0].clickCheckBox();
    const alert1 = await p.clickSelect();
    assert(await alert1.getText() === 'まぐろ');

    await alert1.accept();
    await p.clickAllCheck();

    const alert2 = await p.clickSelect();
    assert(await alert2.getText() === 'まぐろ,はまち,かつお');
  });

  it('全部チェックを外すとすべてのアイテムが選択解除になること', async () => {
    const p =  new FishesList(driver);
    await p.open();
    await p.waitForRowToFinishLoading();

    const rows = await p.getRows();
    await rows[0].clickCheckBox();
    await rows[1].clickCheckBox();
    await rows[2].clickCheckBox();

    const alert1 = await p.clickSelect();
    assert(await alert1.getText() === 'まぐろ,はまち,かつお');

    await alert1.accept();
    await p.clickAllCheck();

    const alert2 = await p.clickSelect();
    assert(await alert2.getText() === 'せんたくしてください');
  });
});
